"""Check and optionally stage the pinned BIOL-1 distribution inventory."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
AUDITED = "19b2fd0647ba55de77fbbb385eda7a4ba6fe05de"
ORGANIZED = {
    "course", "dashboards", "homework", "labs", "module_keys", "modules",
    "practice_tests", "review_materials", "slides",
}
MIRRORS = ("full_flat", "ALL_FILES")
MODULE = re.compile(r"module-[0-9]{2}-.+")
FIGURE = "distribution-coverage.png"
ALT = "Counts of tracked paths and distinct Git blob IDs for the organized resources and the two bulk views."


def inventory():
    raw = subprocess.check_output(
        ["git", "ls-tree", "-rz", AUDITED],
        cwd=ROOT,
        env={**os.environ, "GIT_NO_LAZY_FETCH": "1"},
    )
    groups = defaultdict(dict)
    for record in filter(None, raw.split(b"\0")):
        metadata, path = record.split(b"\t", 1)
        _, kind, object_id = metadata.decode("ascii").split()
        top, _, relative = os.fsdecode(path).partition("/")
        if kind == "blob" and (top in ORGANIZED or top in MIRRORS or MODULE.fullmatch(top)):
            groups[top][relative] = object_id
    return groups


def format_pairs(paths):
    pdf = {name[:-4] for name in paths if name.endswith(".pdf")}
    docx = {name[:-5] for name in paths if name.endswith(".docx")}
    if pdf != docx:
        raise ValueError("An expected PDF or DOCX variant is missing")
    return len(pdf)


def summarize(groups):
    bundles = groups["modules"]
    module_names = {path.split("/", 1)[0] for path in bundles}
    root_modules = {name for name in groups if MODULE.fullmatch(name)}
    if module_names != root_modules:
        raise ValueError("Root quiz folders and module bundles differ")
    quizzes = {
        f"{module}/{path}": object_id
        for module in root_modules
        for path, object_id in groups[module].items()
    }
    quiz_matches = sum(bundles.get(path) == object_id for path, object_id in quizzes.items())
    organized = [
        object_id
        for name, paths in groups.items()
        if name not in MIRRORS
        for object_id in paths.values()
    ]
    organized_ids = set(organized)
    mirror_counts = {}
    for mirror in MIRRORS:
        paths = groups[mirror]
        objects = set(paths.values())
        mirror_counts[mirror] = {
            "paths": len(paths),
            "unique_blobs": len(objects),
            "missing_from_organized": len(organized_ids - objects),
            "extra_to_organized": len(objects - organized_ids),
        }
    dashboards = groups["dashboards"]
    practice_tests = groups["practice_tests"]
    return {
        "audited_commit": AUDITED,
        "course_files": len(groups["course"]),
        "course_format_pairs": format_pairs(groups["course"]),
        "module_bundles": len(module_names),
        "module_paths": len(bundles),
        "quiz_paths": len(quizzes),
        "quiz_matched_paths": quiz_matches,
        "quiz_format_pairs": sum(format_pairs(groups[name]) for name in root_modules),
        "lab_format_pairs": format_pairs(groups["labs"]),
        "dashboard_files": len(dashboards),
        "lab_dashboards": sum(path.startswith("lab-") and path.endswith(".html") for path in dashboards),
        "review_dashboards": sum(path.startswith("exam-") and path.endswith(".html") for path in dashboards),
        "practice_sets": sum(re.fullmatch(r"practice-test-[0-9]{2}\.pdf", path) is not None for path in practice_tests),
        "practice_paths": len(practice_tests),
        "practice_formats": len({PurePosixPath(path).suffix for path in practice_tests}),
        "review_worksheet_pairs": format_pairs(groups["review_materials"]),
        "slide_pdfs": sum(path.endswith(".pdf") for path in groups["slides"]),
        "organized": {"paths": len(organized), "unique_blobs": len(organized_ids)},
        "mirrors": mirror_counts,
    }


def stage(results):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    output = ROOT / "output"
    figures = output / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    (output / "inventory.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    counts = [results["organized"], *(results["mirrors"][name] for name in MIRRORS)]
    labels = ["Organized resources", "full_flat", "ALL_FILES"]
    fig, ax = plt.subplots(figsize=(7.0, 3.0), layout="constrained")
    y = list(range(len(labels)))
    paths = ax.barh([n - 0.18 for n in y], [item["paths"] for item in counts], 0.32,
                    color="#214d72", label="Tracked paths")
    unique = ax.barh([n + 0.18 for n in y], [item["unique_blobs"] for item in counts], 0.32,
                     color="#b65929", label="Distinct file objects")
    ax.bar_label(paths, padding=4)
    ax.bar_label(unique, padding=4)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 850)
    ax.set_xlabel("Count")
    ax.legend(loc="upper right", frameon=False)
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.savefig(figures / FIGURE, dpi=220)
    plt.close(fig)

    registry = {"fig:distribution-coverage": {
        "label": "fig:distribution-coverage",
        "filename": FIGURE,
        "caption": ALT,
        "metadata": {"alt_text": ALT},
        "generated_by": "docs/inventory.py",
    }}
    (figures / "figure_registry.json").write_text(
        json.dumps(registry, indent=2) + "\n", encoding="utf-8"
    )
    source = ROOT / "docs" / "manuscript"
    manuscript = output / "manuscript"
    manuscript.mkdir(exist_ok=True)
    for section in sorted(source.glob("[0-9][0-9]_*.md")):
        text = section.read_text(encoding="utf-8")
        (manuscript / section.name).write_text(
            text.replace("../../output/figures/", "../figures/"), encoding="utf-8"
        )
    for name in ("preamble.md", "references.bib"):
        shutil.copyfile(source / name, manuscript / name)
    config = (source / "config.yaml").read_text(encoding="utf-8")
    (manuscript / "config.yaml").write_text(
        "# Generated manuscript ordering\n" + config, encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", action="store_true", help="also prepare figure and manuscript outputs")
    args = parser.parse_args()
    results = summarize(inventory())
    if args.stage:
        stage(results)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
