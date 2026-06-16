#!/usr/bin/env python3
"""Top-level publish entrypoint. Reads publish.toml and delegates to publish_all.py.

Supports automatic git operations:
- Commit PUBLISHED changes to cr-bio
- Subtree push active PUBLISHED course prefixes to public repos
"""

import argparse
import logging
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SOFTWARE_DIR = REPO_ROOT / "software"
CONFIG_PATH = REPO_ROOT / "publish.toml"
PUBLISH_SCRIPT = SOFTWARE_DIR / "scripts" / "publish_all.py"

sys.path.insert(0, str(SOFTWARE_DIR))
from src.shared.runtime import configure_runtime_environment  # noqa: E402

configure_runtime_environment()

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


def load_config() -> dict:
    with open(CONFIG_PATH, "rb") as f:
        return tomllib.load(f)


def enabled_formats(config: dict) -> list[str]:
    return [fmt for fmt, on in config["publish"]["formats"].items() if on]


def build_args(config: dict, override_formats: str | None = None) -> list[str]:
    pub = config["publish"]
    pipeline = pub.get("pipeline", {})
    args: list[str] = []

    if pub.get("clean"):
        args.append("--clean")
        args.append("--clean-source-outputs")
    if pub.get("verbose"):
        args.append("--verbose")

    # Pipeline stage toggles
    if not pipeline.get("generate", True):
        args.append("--skip-generation")
    if not pipeline.get("publish", True):
        args.append("--skip-publish")
    if not pipeline.get("copy_extras", True):
        args.append("--skip-copy-extras")
    if not pipeline.get("flatten", True):
        args.append("--skip-flatten")
    if not pipeline.get("validate", True):
        args.append("--skip-validate")
    if pipeline.get("strict_dashboards", False):
        args.append("--strict-dashboards")

    # Per-course lab settings: skip labs if ALL enabled courses have include_labs=false
    courses = pub.get("courses", {})
    enabled_courses = {k: v for k, v in courses.items() if v.get("enabled", True)}
    if enabled_courses and all(not c.get("include_labs", True) for c in enabled_courses.values()):
        args.append("--skip-labs")

    # Formats
    if override_formats:
        args.extend(["--formats", override_formats])
    else:
        fmts = enabled_formats(config)
        if fmts:
            args.extend(["--formats", ",".join(fmts)])

    # Module and lab limits per course
    for course_name, course_cfg in enabled_courses.items():
        if course_cfg.get("max_module") is not None:
            args.extend(["--max-module", f"{course_name}:{course_cfg['max_module']}"])
        if course_cfg.get("max_lab") is not None:
            args.extend(["--max-lab", f"{course_name}:{course_cfg['max_lab']}"])

    return args


def run_cmd(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    log.info(f"  → {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=cwd or REPO_ROOT, capture_output=True, text=True, check=check)


def setup_git_remotes(config: dict) -> bool:
    """Ensure git remotes are configured for all repos."""
    git_cfg = config["publish"].get("git", {})
    if not git_cfg.get("enabled", True):
        return True

    repos = git_cfg.get("repos", {})
    existing = subprocess.run(
        ["git", "remote", "-v"], cwd=REPO_ROOT, capture_output=True, text=True
    ).stdout

    success = True
    for name, repo_cfg in repos.items():
        remote = repo_cfg.get("remote", name)
        url = repo_cfg.get("url", "")
        
        if remote not in existing:
            log.info(f"Adding git remote: {remote} → {url}")
            result = run_cmd(["git", "remote", "add", remote, url], check=False)
            if result.returncode != 0:
                log.warning(f"  Failed to add remote {remote}: {result.stderr.strip()}")
                success = False
        else:
            log.info(f"Git remote exists: {remote}")
    
    return success


def git_has_changes() -> bool:
    """Check if there are uncommitted changes in PUBLISHED/."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "PUBLISHED/"],
        cwd=REPO_ROOT, capture_output=True, text=True
    )
    return bool(result.stdout.strip())


def git_commit(config: dict) -> bool:
    """Commit PUBLISHED changes if auto_commit is enabled."""
    git_cfg = config["publish"].get("git", {})
    if not git_cfg.get("auto_commit", True):
        log.info("Auto-commit disabled, skipping...")
        return True

    if not git_has_changes():
        log.info("No changes to commit in PUBLISHED/")
        return True

    message = git_cfg.get("commit_message", "Update published course materials")
    
    log.info("Committing PUBLISHED changes...")
    run_cmd(["git", "add", "-A", "PUBLISHED/"])
    run_cmd(["git", "add", "-A", "."])  # Include any other tracked changes
    result = run_cmd(["git", "commit", "-m", message], check=False)
    
    if result.returncode != 0:
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            log.info("Nothing to commit")
            return True
        log.error(f"Commit failed: {result.stderr.strip()}")
        return False
    
    log.info("Committed successfully")
    return True


def git_push_repos(config: dict) -> bool:
    """Push to all configured repos with detailed logging."""
    git_cfg = config["publish"].get("git", {})
    if not git_cfg.get("enabled", True):
        log.info("Git operations disabled in config")
        return True

    repos = git_cfg.get("repos", {})
    success = True
    pushed_repos = []
    skipped_repos = []
    failed_repos = []

    log.info(f"\nConfigured repositories: {len(repos)}")

    for name, repo_cfg in repos.items():
        if not repo_cfg.get("push", True):
            log.info(f"  ⏭  {name}: push disabled, skipping")
            skipped_repos.append(name)
            continue

        remote = repo_cfg.get("remote", name)
        branch = repo_cfg.get("branch", "main")
        prefix = repo_cfg.get("prefix")  # For subtree push
        force = repo_cfg.get("force", False)
        url = repo_cfg.get("url", "")

        log.info(f"\n{'='*50}")
        log.info(f"PUSHING: {name}")
        log.info(f"  Remote: {remote} → {url}")
        log.info(f"  Branch: {branch}")
        if prefix:
            log.info(f"  Mode:   subtree (prefix: {prefix})")
        if force:
            log.info(f"  Force:  enabled")
        log.info(f"{'='*50}")

        if prefix:
            # Subtree push for course repos
            log.info(f"Stage 1: Subtree split from {prefix}...")
            split_result = subprocess.run(
                ["git", "subtree", "split", f"--prefix={prefix}"],
                cwd=REPO_ROOT, capture_output=True, text=True
            )
            if split_result.returncode != 0:
                log.error(f"  ✗ Subtree split failed: {split_result.stderr.strip()}")
                failed_repos.append((name, "subtree split failed"))
                success = False
                continue

            commit_sha = split_result.stdout.strip()
            log.info(f"  Subtree commit: {commit_sha[:12]}...")
            
            log.info(f"Stage 2: Pushing to {remote}/{branch}...")
            push_cmd = ["git", "push", remote, f"{commit_sha}:{branch}"]
            if force:
                push_cmd.append("--force")
            
            log.info(f"  Command: {' '.join(push_cmd)}")
            result = run_cmd(push_cmd, check=False)
        else:
            # Regular push for main repo
            log.info(f"Pushing directly to {remote}/{branch}...")
            push_cmd = ["git", "push", remote, branch]
            if force:
                push_cmd.append("--force")
            log.info(f"  Command: {' '.join(push_cmd)}")
            result = run_cmd(push_cmd, check=False)

        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip()
            log.error(f"  ✗ Push failed: {error_msg}")
            failed_repos.append((name, error_msg[:50]))
            success = False
        else:
            # Check for actual push output
            output = result.stdout.strip() or result.stderr.strip()
            if "Everything up-to-date" in output:
                log.info(f"  ✓ {name}: already up-to-date")
            else:
                log.info(f"  ✓ {name}: pushed successfully")
            pushed_repos.append(name)

    # Summary
    log.info(f"\n{'='*50}")
    log.info("GIT PUSH SUMMARY")
    log.info(f"{'='*50}")
    log.info(f"  Pushed:  {len(pushed_repos)} repos")
    for repo in pushed_repos:
        log.info(f"           ✓ {repo}")
    if skipped_repos:
        log.info(f"  Skipped: {len(skipped_repos)} repos")
    if failed_repos:
        log.info(f"  Failed:  {len(failed_repos)} repos")
        for repo, reason in failed_repos:
            log.info(f"           ✗ {repo}: {reason}")
    log.info(f"{'='*50}\n")

    return success


def flatten_all_files(config: dict) -> None:
    """Copy and flatten all output files into an ALL_FILES/ subdirectory at each PUBLISHED course level.
    
    Every file from every subdirectory of PUBLISHED/<course> is copied into
    PUBLISHED/<course>/ALL_FILES/. When filenames collide across subdirectories
    the source subdirectory name is prepended (e.g., 'labs_lab-01.pdf').
    """
    pub = config["publish"]
    courses = pub.get("courses", {})
    published_root = REPO_ROOT / "PUBLISHED"

    total_copied = 0
    for course_name, course_cfg in courses.items():
        if not course_cfg.get("enabled", True):
            continue

        course_dir = published_root / course_name
        if not course_dir.is_dir():
            log.info(f"  {course_name}: PUBLISHED directory not found, skipping")
            continue

        all_files_dir = course_dir / "ALL_FILES"
        # Clean and recreate
        if all_files_dir.exists():
            shutil.rmtree(all_files_dir)
        all_files_dir.mkdir(parents=True)

        # Collect every file from every subdirectory (skip ALL_FILES itself)
        seen_names: dict[str, str] = {}  # filename -> source subdir
        copied = 0
        for sub in sorted(course_dir.iterdir()):
            if not sub.is_dir() or sub.name == "ALL_FILES":
                continue
            for src_file in sorted(sub.rglob("*")):
                if not src_file.is_file():
                    continue
                fname = src_file.name
                if fname in seen_names:
                    # Name collision — prefix with source subdirectory
                    fname = f"{sub.name}_{fname}"
                else:
                    seen_names[fname] = sub.name
                shutil.copy2(src_file, all_files_dir / fname)
                copied += 1

        log.info(f"  {course_name}: {copied} files → ALL_FILES/")
        total_copied += copied

    log.info(f"  ✅ Flattened {total_copied} total files into ALL_FILES/")


def main():
    parser = argparse.ArgumentParser(description="Publish courses using publish.toml config")
    parser.add_argument("--dry-run", action="store_true", help="Show command without executing")
    parser.add_argument("--override-formats", type=str, default=None,
                        help="Override config formats (comma-separated, e.g. pdf,docx,md)")
    parser.add_argument("--setup-git", action="store_true", 
                        help="Set up git remotes from config and exit")
    parser.add_argument("--git-only", action="store_true",
                        help="Skip generation, only run git commit and push")
    parser.add_argument("--skip-git", action="store_true",
                        help="Skip git operations even if enabled in config")
    cli = parser.parse_args()

    config = load_config()

    # Setup git remotes only
    if cli.setup_git:
        log.info("Setting up git remotes from publish.toml...")
        setup_git_remotes(config)
        return

    # Git-only mode (skip generation)
    if cli.git_only:
        log.info("Git-only mode: skipping generation, running git operations...")
        if git_commit(config) and git_push_repos(config):
            log.info("\n✓ Git operations completed successfully")
        else:
            log.error("\n✗ Git operations failed")
            sys.exit(1)
        return

    args = build_args(config, cli.override_formats)
    cmd = ["uv", "run", "python", str(PUBLISH_SCRIPT)] + args

    if cli.dry_run:
        pub = config["publish"]
        pipeline = pub.get("pipeline", {})
        courses_cfg = pub.get("courses", {})
        git_cfg = pub.get("git", {})

        print("publish.toml config loaded:")
        print(f"  formats:  {enabled_formats(config)}")
        print(f"  clean:    {pub.get('clean')}")
        print(f"  verbose:  {pub.get('verbose')}")
        print(f"  pipeline: generate={pipeline.get('generate', True)}, "
              f"publish={pipeline.get('publish', True)}, "
              f"copy_extras={pipeline.get('copy_extras', True)}, "
              f"flatten={pipeline.get('flatten', True)}, "
              f"validate={pipeline.get('validate', True)}, "
              f"git_push={pipeline.get('git_push', False)}")
        for name, course in courses_cfg.items():
            print(f"  {name}: enabled={course.get('enabled', True)}, "
                  f"labs={course.get('include_labs', True)}, "
                  f"syllabus={course.get('include_syllabus', True)}, "
                  f"dashboards={course.get('include_dashboards', True)}, "
                  f"archive={course.get('archive_path', '')}")
        
        # Show git config
        if git_cfg.get("enabled", True):
            print("\nGit configuration:")
            print(f"  auto_commit: {git_cfg.get('auto_commit', True)}")
            print(f"  git_push:    {pipeline.get('git_push', False)}")
            for name, repo in git_cfg.get("repos", {}).items():
                push_status = "push" if repo.get("push", True) else "skip"
                force_status = " (force)" if repo.get("force", False) else ""
                prefix = f" [subtree: {repo.get('prefix')}]" if repo.get("prefix") else ""
                print(f"  {name}: {repo.get('remote')} → {repo.get('branch')} [{push_status}{force_status}]{prefix}")
        
        print("\nWould run (cwd: software/):")
        print(f"  {' '.join(cmd)}")
        return

    # Run the publish pipeline
    log.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT / "software")
    
    if result.returncode != 0:
        log.error("Publish pipeline failed")
        sys.exit(result.returncode)

    # Flatten all files into ALL_FILES/ (if enabled)
    pipeline = config["publish"].get("pipeline", {})
    if pipeline.get("all_files", True):
        log.info("\n📂 STEP 7: Flattening all files into ALL_FILES/")
        flatten_all_files(config)

    # Git operations (if enabled)
    pipeline = config["publish"].get("pipeline", {})
    if pipeline.get("git_push", False) and not cli.skip_git:
        log.info("\n" + "="*50)
        log.info("Running git operations...")
        log.info("="*50)
        
        setup_git_remotes(config)
        
        if not git_commit(config):
            log.error("Git commit failed")
            sys.exit(1)
        
        if not git_push_repos(config):
            log.error("Git push failed")
            sys.exit(1)
        
        log.info("\n✓ All git operations completed successfully")

    log.info("\n" + "="*70)
    published = REPO_ROOT / "PUBLISHED"
    total = sum(1 for _ in published.rglob("*") if _.is_file()) if published.is_dir() else 0
    courses_cfg = config["publish"].get("courses", {})
    log.info("  PUBLISH COMPLETE")
    log.info("="*70)
    log.info(f"  PUBLISHED/ total files (recursive, includes ALL_FILES/ duplicates): {total}")
    for cname, course_cfg in courses_cfg.items():
        if not course_cfg.get("enabled", True):
            continue
        cdir = published / cname
        if cdir.is_dir():
            ccount = sum(1 for _ in cdir.rglob("*") if _.is_file())
            all_dir = cdir / "ALL_FILES"
            all_count = sum(1 for _ in all_dir.rglob("*") if _.is_file()) if all_dir.is_dir() else 0
            unique_count = ccount - all_count
            log.info(
                f"    {cname}: {ccount} files total "
                f"({unique_count} unique + {all_count} duplicated in ALL_FILES/)"
            )
    log.info("  Note: validation 'Total files' line earlier counts the same tree")
    log.info("        but BEFORE ALL_FILES/ was created; both numbers are correct.")
    log.info("="*70)


if __name__ == "__main__":
    main()
