"""BIOL-1 module → LectureCreate video integration.

Generates LectureCreate-compatible YAML manifests from structured
module.toml files, with SVG → PNG asset conversion and a thin
subprocess invocation layer for rendering.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from src.module_content.main import ModuleContent, Term, load_module_content

__all__ = [
    "LECTURECREATE_BIN",
    "build_combined_lecture_yaml",
    "build_module_lecture_yaml",
    "enrich_narrations_with_llm",
    "render_module_video",
    "term_pages",
]


LECTURECREATE_BIN = "lecturecreate"

# ---------------------------------------------------------------------------
# YAML generation
# ---------------------------------------------------------------------------


def _yaml_str(value: str) -> str:
    """Quote a string safely for embedding in YAML."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _yaml_list(items: list[str], indent: int = 0) -> str:
    """Render a list of strings as a YAML block."""
    prefix = " " * indent
    if not items:
        return f"{prefix}[]"
    lines = [f"{prefix}- {_yaml_str(item)}" for item in items]
    return "\n".join(lines)


def _yaml_block(key: str, value: str | float, indent: int = 0) -> str:
    """Render a key: value pair."""
    prefix = " " * indent
    if isinstance(value, bool):
        return f"{prefix}{key}: {'true' if value else 'false'}"
    if isinstance(value, (int, float)):
        return f"{prefix}{key}: {value}"
    return f"{prefix}{key}: {_yaml_str(value)}"


def term_pages(module: ModuleContent, page_size: int = 3) -> list[tuple[Term, ...]]:
    """Split a module's terms into readable recap pages.

    Three definitions per slide gives long definitions enough breathing room
    at 1920×1080 while ensuring every authored term remains in the lecture.
    """
    if page_size < 1:
        raise ValueError("page_size must be positive")
    return [
        module.terms[start : start + page_size] for start in range(0, len(module.terms), page_size)
    ]


def build_module_lecture_yaml(
    module_dir: Path | str,
    output_dir: Path | str,
    lecturecreate_config_path: Path | str | None = None,
) -> str:
    """Build a LectureCreate YAML manifest from a BIOL-1 module manifest.

    Parameters
    ----------
    module_dir:
        Path to a ``module-NN-topic/`` directory containing ``module.toml``.
    output_dir:
        Directory where PNG assets and the YAML file will be written.
    lecturecreate_config_path:
        Optional path to a LectureCreate render config YAML.

    Returns
    -------
    str
        The generated YAML string, ready to write to disk.
    """
    module = load_module_content(module_dir)
    lines: list[str] = []
    _emit = lines.append

    # --- Header ---
    _emit(f"# Generated from {module.slug}/module.toml — do not hand-edit")
    _emit(f"title: {_yaml_str(f'BIOL-1 Module {module.number:02d}: {module.title}')}")
    _emit(f"subtitle: {_yaml_str('College of the Redwoods — Pelican Bay')}")
    _emit("width: 1920")
    _emit("height: 1080")
    _emit("fps: 30")
    if lecturecreate_config_path:
        _emit(
            f"# Render with: lecturecreate from-yaml <this-file> --config {lecturecreate_config_path}"
        )
    _emit("")

    # --- Series metadata ---
    _emit("metadata:")
    _emit(f"  author: {_yaml_str('Dr. Daniel Ari Friedman')}")
    _emit(f"  topic: {_yaml_str(module.title)}")
    _emit(f"  series: {_yaml_str('BIOL-1: General Biology')}")
    _emit(f"  series_index: {module.number}")
    _emit("  series_total: 16")
    _emit(f"  lab: {_yaml_str(_lab_display_name(module))}")
    _emit("")

    # --- Single section per module ---
    _emit("sections:")
    _emit(f"- id: {_yaml_str(module.slug)}")
    _emit(f"  title: {_yaml_str(f'Module {module.number:02d}: {module.title}')}")
    _emit("  objectives:")
    for obj in module.learning_objectives:
        _emit(f"    - {_yaml_str(obj)}")
    _emit("  beats:")
    _emit("")

    # --- Beat 1: Title ---
    _emit(f"  - id: {_yaml_str(f'{module.slug}_title')}")
    _emit(f"    narration: {_yaml_str(_title_narration(module))}")
    _emit("    visual:")
    _emit("      kind: title")
    _emit(f"      title: {_yaml_str(f'Module {module.number:02d}: {module.title}')}")
    lab_display = _lab_display_name(module)
    _emit(f"      subtitle: {_yaml_str(f'BIOL-1 General Biology  |  Lab: {lab_display}')}")
    _emit("")

    # --- Beat 2: Learning Objectives ---
    _emit(f"  - id: {_yaml_str(f'{module.slug}_objectives')}")
    _emit(f"    narration: {_yaml_str(_objectives_narration(module))}")
    _emit("    visual:")
    _emit("      kind: objectives")
    _emit(f"      title: {_yaml_str('Learning Objectives')}")
    _emit("      bullets:")
    for obj in module.learning_objectives:
        _emit(f"        - {_yaml_str(obj)}")
    _emit("")

    # --- Beat 3: Topics sequence ---
    _emit(f"  - id: {_yaml_str(f'{module.slug}_topics')}")
    _emit(f"    narration: {_yaml_str(_topics_narration(module))}")
    _emit("    visual:")
    _emit("      kind: bullets")
    _emit(f"      title: {_yaml_str('Topic Sequence')}")
    _emit("      bullets:")
    for topic in module.topics:
        _emit(f"        - {_yaml_str(topic)}")
    _emit("")

    # --- Beat 4: Concept Map (IMAGE) ---
    concept_svg = f"module-{module.number:02d}-concept-map.svg"
    _emit(f"  - id: {_yaml_str(f'{module.slug}_concept_map')}")
    _emit(f"    narration: {_yaml_str(_concept_map_narration(module))}")
    _emit("    visual:")
    _emit("      kind: image")
    _emit(f"      title: {_yaml_str('Concept Map')}")
    _emit(f"      subtitle: {_yaml_str('How the ideas connect')}")
    _emit(f"      image_path: {_yaml_str(str(Path('png') / concept_svg.replace('.svg', '.png')))}")
    _emit("")

    # --- Beat 5: Process Model (IMAGE) ---
    process_svg = f"module-{module.number:02d}-process-model.svg"
    _emit(f"  - id: {_yaml_str(f'{module.slug}_process_model')}")
    _emit(f"    narration: {_yaml_str(_process_model_narration(module))}")
    _emit("    visual:")
    _emit("      kind: image")
    _emit(f"      title: {_yaml_str('Process Model')}")
    _emit(f"      subtitle: {_yaml_str('Reasoning sequence')}")
    _emit(f"      image_path: {_yaml_str(str(Path('png') / process_svg.replace('.svg', '.png')))}")
    _emit("")

    # --- Beat 6: Apply the Idea (claim → evidence → revision) ---
    _emit(f"  - id: {_yaml_str(f'{module.slug}_application')}")
    _emit(f"    narration: {_yaml_str(_application_narration(module))}")
    _emit("    visual:")
    _emit("      kind: bullets")
    _emit(f"      title: {_yaml_str('Apply the Idea')}")
    _emit("      bullets:")
    _emit(f"        - {_yaml_str(f'Observation: {module.learning_questions[0]}')}")
    _emit(f"        - {_yaml_str(f'Claim: {module.contents[0]}')}")
    _emit(f"        - {_yaml_str(f'Evidence check: {module.practice_quiz[0].explanation}')}")
    _emit(
        f"        - {_yaml_str('Revision: if the evidence contradicts the claim, name the biological mechanism that must change.')}"
    )
    _emit("")

    # --- Beats 7–8: Key Terms (paginated for readability) ---
    pages = term_pages(module)
    for page_number, page in enumerate(pages, 1):
        _emit(f"  - id: {_yaml_str(f'{module.slug}_terms_{page_number:02d}')}")
        _emit(f"    narration: {_yaml_str(_terms_page_narration(page, page_number, len(pages)))}")
        _emit("    visual:")
        _emit("      kind: recap")
        title = "Key Terms" if len(pages) == 1 else f"Key Terms ({page_number}/{len(pages)})"
        _emit(f"      title: {_yaml_str(title)}")
        _emit("      bullets:")
        for term in page:
            _emit(f"        - {_yaml_str(f'{term.name}: {term.definition}')}")
        _emit("")

    # --- Beat 7: Lab Connection ---
    _emit(f"  - id: {_yaml_str(f'{module.slug}_lab')}")
    _emit(f"    narration: {_yaml_str(_lab_narration(module))}")
    _emit("    visual:")
    _emit("      kind: bullets")
    _emit(f"      title: {_yaml_str('Lab Connection')}")
    _emit("      bullets:")
    lab_name = _lab_display_name(module)
    _emit(f"        - {_yaml_str(f'Lab: {lab_name}')}")
    _emit(f"        - {_yaml_str(f'Evidence surface for: {module.topics[0]}')}")
    _emit(f"        - {_yaml_str('Connect module ideas to hands-on evidence')}")
    _emit("")

    # --- Beat 8: Lab Evidence (IMAGE) ---
    lab_svg = f"module-{module.number:02d}-lab-evidence.svg"
    _emit(f"  - id: {_yaml_str(f'{module.slug}_lab_evidence')}")
    _emit(f"    narration: {_yaml_str(_lab_evidence_narration(module))}")
    _emit("    visual:")
    _emit("      kind: image")
    _emit(f"      title: {_yaml_str('Lab Evidence')}")
    _emit(f"      subtitle: {_yaml_str('What the lab shows')}")
    _emit(f"      image_path: {_yaml_str(str(Path('png') / lab_svg.replace('.svg', '.png')))}")
    _emit("")

    # --- Beat 9: Retrieval Card (IMAGE) ---
    retrieval_svg = f"module-{module.number:02d}-retrieval-card.svg"
    _emit(f"  - id: {_yaml_str(f'{module.slug}_retrieval')}")
    _emit(f"    narration: {_yaml_str(_retrieval_narration(module))}")
    _emit("    visual:")
    _emit("      kind: image")
    _emit(f"      title: {_yaml_str('Retrieval Practice')}")
    _emit(f"      subtitle: {_yaml_str('Answer without notes first')}")
    _emit(
        f"      image_path: {_yaml_str(str(Path('png') / retrieval_svg.replace('.svg', '.png')))}"
    )
    _emit("")

    # --- Beat 10: Practice Quiz ---
    _emit(f"  - id: {_yaml_str(f'{module.slug}_quiz')}")
    _emit(f"    narration: {_yaml_str(_quiz_narration(module))}")
    _emit("    visual:")
    _emit("      kind: checkpoint")
    _emit(f"      title: {_yaml_str('Practice Quiz Bridge')}")
    _emit("      bullets:")
    for i, quiz in enumerate(module.practice_quiz[:4], 1):
        _emit(f"        - {_yaml_str(f'Q{i}: {quiz.question}')}")
    _emit("")

    # --- Beat 11: Study Move (retrieval protocol) ---
    _emit(f"  - id: {_yaml_str(f'{module.slug}_study_move')}")
    _emit(f"    narration: {_yaml_str(_study_move_narration(module))}")
    _emit("    visual:")
    _emit("      kind: bullets")
    _emit(f"      title: {_yaml_str('Active Study Protocol')}")
    _emit("      bullets:")
    for tip in module.study_tips[:3]:
        _emit(f"        - {_yaml_str(tip)}")
    _emit(f"        - {_yaml_str('Close the notes. Answer the exit question from memory.')}")
    _emit(f"        - {_yaml_str(f'Exit question: {module.learning_questions[-1]}')}")
    _emit(
        f"        - {_yaml_str('Check your answer against the module keys; revise until the chain of evidence is clear.')}"
    )
    _emit("")

    # --- Beat 12: Synthesis and Revision Rule ---
    _emit(f"  - id: {_yaml_str(f'{module.slug}_synthesis')}")
    _emit(f"    narration: {_yaml_str(_synthesis_narration(module))}")
    _emit("    visual:")
    _emit("      kind: bullets")
    _emit(f"      title: {_yaml_str('Synthesis and Revision')}")
    _emit("      bullets:")
    _emit(
        f"        - {_yaml_str(f'Explain {module.topics[0].lower()} using evidence from the {lab_name} lab')}"
    )
    all_terms = ", ".join(term.name for term in module.terms)
    _emit(f"        - {_yaml_str(f'Must include: {all_terms}')}")
    _emit(
        f"        - {_yaml_str('Revision rule: if the lab evidence contradicts your explanation, name the mechanism that must change.')}"
    )
    _emit(f"        - {_yaml_str('What evidence would change your explanation?')}")
    _emit("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Narration helpers — compact single-paragraph scripts per beat
# ---------------------------------------------------------------------------


def _lab_display_name(module: ModuleContent) -> str:
    """Return a human-readable lab name from the module's lab filename."""
    name = module.lab.replace(".md", "").replace("_", " ").replace("-", " ")
    # Capitalize each word
    return " ".join(w.capitalize() for w in name.split())


def _central_claim(module: ModuleContent) -> str:
    """Return the concept map central claim if available, else the title."""
    for img in module.generated_images:
        if img.concept_map and img.concept_map.central_claim.strip():
            return img.concept_map.central_claim.strip()
    return module.title


def _title_narration(module: ModuleContent) -> str:
    claim = _central_claim(module)
    lab = _lab_display_name(module)
    return (
        f"Welcome to BIOL-1 General Biology at College of the Redwoods, Pelican Bay. "
        f"Module {module.number:02d}: {module.title}. "
        f"The connected lab is {lab}. "
        f"Here is the central idea: {claim} Let us begin."
    )


def _objectives_narration(module: ModuleContent) -> str:
    items = "; ".join(obj.rstrip(".") for obj in module.learning_objectives)
    return (
        f"By the end of this module you should be able to: {items}. "
        f"Keep these objectives in mind as you work through the material."
    )


def _topics_narration(module: ModuleContent) -> str:
    pairs = [f"{t} — {c.rstrip('.')}" for t, c in zip(module.topics, module.contents)]
    return (
        f"This module covers {len(module.topics)} topics. "
        + ". ".join(pairs)
        + ". Each topic builds on the one before it, forming a coherent explanation."
    )


def _concept_map_narration(module: ModuleContent) -> str:
    claim = _central_claim(module)
    return (
        f"Here is the concept map for module {module.number:02d}. "
        f"The central claim is: {claim} "
        f"Notice how each node connects to the others. "
        f"This is the structure of biological reasoning — not a list to memorize, but a map of how ideas support each other."
    )


def _process_model_narration(module: ModuleContent) -> str:
    lab = _lab_display_name(module)
    return (
        f"This process model shows the reasoning sequence for {module.title.lower()}. "
        f"Follow the stages from inputs to outputs. "
        f"The {lab} lab gives you evidence to test each stage. "
        f"At each transition, ask: what would change my mind about this step?"
    )


def _terms_page_narration(terms: tuple[Term, ...], page_number: int, page_total: int) -> str:
    terms_list = ", ".join(term.name for term in terms)
    page_label = "" if page_total == 1 else f" (page {page_number} of {page_total})"
    return (
        f"Key terms for this module{page_label} include {terms_list}. "
        f"Treat each term as a handle for reasoning — "
        f"a term should help you explain a claim or observation, not just label it."
    )


def _application_narration(module: ModuleContent) -> str:
    """Turn the first module question into a concrete claim-evidence move."""
    question = module.learning_questions[0]
    content = module.contents[0].rstrip(".")
    explanation = module.practice_quiz[0].explanation.rstrip(".")
    return (
        f"Now apply the module instead of only repeating its vocabulary. Start with a question: "
        f"{question} Treat that question as an observation that needs an explanation. "
        f"A useful first claim is: {content}. Then ask what evidence could support or challenge it. "
        f"The first practice check reminds us that {explanation}. "
        f"This claim, evidence, and revision cycle is the transferable skill for the module."
    )


def _lab_narration(module: ModuleContent) -> str:
    lab = _lab_display_name(module)
    return (
        f"The lab connected to this module is {lab}. "
        f"The evidence you collect should test or illustrate {module.topics[0].lower()}. "
        f"You should leave the lab with a concrete observation, comparison, or model "
        f"tied directly to the module claim."
    )


def _lab_evidence_narration(module: ModuleContent) -> str:
    lab = _lab_display_name(module)
    return (
        f"The {lab} lab produces concrete evidence for this module. "
        f"Focus on the measurable outcome: what changed, by how much, and why it matters. "
        f"Connect the lab result back to the central claim. "
        f"A strong answer names the variable, the observation, and the biological mechanism."
    )


def _retrieval_narration(module: ModuleContent) -> str:
    return (
        "Pause here for retrieval practice. "
        "Answer the prompts without looking at your notes first, then compare to the checks. "
        "Retrieval practice is one of the most effective study strategies — "
        "it strengthens memory more than re-reading."
    )


def _quiz_narration(module: ModuleContent) -> str:
    answers = ", ".join(f"{i}={q.answer}" for i, q in enumerate(module.practice_quiz[:4], 1))
    return (
        f"Use these practice quiz questions as formative feedback. "
        f"Answer key: {answers}. "
        f"If you miss a question, return to the module keys and find the evidence "
        f"that supports the correct answer."
    )


def _study_move_narration(module: ModuleContent) -> str:
    """Give students a short, actionable study sequence grounded in the module."""
    tips = "; ".join(t.rstrip(".") for t in module.study_tips[:3])
    question = module.learning_questions[-1]
    return (
        f"Before you leave this module, make the study work active. {tips}. "
        f"Then answer this exit question without notes: {question} "
        "A strong response names a mechanism, points to evidence, and states what would change the explanation. "
        "If your answer is only a definition list, connect the terms into a cause-and-evidence chain and try again."
    )


def _synthesis_narration(module: ModuleContent) -> str:
    terms_list = ", ".join(term.name for term in module.terms)
    lab = _lab_display_name(module)
    return (
        f"To synthesize this module: explain {module.topics[0].lower()} using evidence from the {lab} lab. "
        f"Your explanation must include {terms_list}. "
        f"Revision prompt: what evidence would change your explanation? "
        "Your final explanation should connect the central claim to a mechanism, an observation, and a revision rule."
    )


def enrich_narrations_with_llm(module: ModuleContent) -> ModuleContent:
    """Enrich narration scripts using an LLM pass reading full module content.

    Reads objectives, terms, topics, contents, quiz data and generates richer,
    more natural narration strings stored in a ``narration_cache`` dict on the
    returned module. This is a non-destructive enrichment — the original
    template-based narration functions still work unchanged.

    The caller should pass ``module.narration_cache`` to the YAML builder
    to use the enriched scripts.
    """
    try:
        from src.llm.client import LLMClient  # type: ignore[import-untyped]
    except ImportError:
        return module  # LLM not available; use template defaults

    prompt = _build_narration_prompt(module)
    try:
        client = LLMClient()
        response = client.query(prompt)
        cache = _parse_narration_response(response, module)
        module.narration_cache = cache  # type: ignore[attr-defined]
    except Exception:
        return module

    return module


def _build_narration_prompt(module: ModuleContent) -> str:
    """Build an LLM prompt for enriching narration."""
    parts = [
        f"Module {module.number:02d}: {module.title}",
        f"Learning objectives: {'; '.join(module.learning_objectives)}",
        f"Topics: {'; '.join(module.topics)}",
        f"Content: {'; '.join(module.contents[:3])}",
        f"Key terms: {'; '.join(f'{t.name}: {t.definition}' for t in module.terms[:5])}",
        f"Lab: {_lab_display_name(module)}",
        "Quiz questions: "
        + "; ".join(f"{q.question} (A: {q.answer})" for q in module.practice_quiz[:3]),
    ]
    body = "\n".join(parts)
    return (
        "You are writing narration for a biology lecture video with a paginated key-term recap. "
        "Generate a concise, natural-spoken narration script for each beat. "
        "Return a JSON object with keys: title, objectives, topics, concept_map, "
        "process_model, terms, lab, retrieval, quiz, synthesis. "
        "Each value should be 1-3 sentences of spoken narration. Keep it instructional "
        "and conversational — the audience is community college biology students.\n\n"
        f"Module content:\n{body}\n\n"
        "Return ONLY valid JSON, no markdown, no explanation."
    )


def _parse_narration_response(response: str, module: ModuleContent) -> dict[str, str]:
    """Parse LLM response into narration cache dict, falling back to defaults."""
    import json as _json

    try:
        data = _json.loads(response)
        expected = {
            "title",
            "objectives",
            "topics",
            "concept_map",
            "process_model",
            "terms",
            "lab",
            "retrieval",
            "quiz",
            "synthesis",
        }
        return {k: v for k, v in data.items() if k in expected and isinstance(v, str)}
    except Exception:
        return {}  # Fall back to template defaults


# ---------------------------------------------------------------------------
# Combined full-course lecture (16 sections, one per module)
# ---------------------------------------------------------------------------


def build_combined_lecture_yaml(
    course_dir: Path | str,
    output_dir: Path | str,
    lecturecreate_config_path: Path | str | None = None,
) -> str:
    """Build a single LectureCreate YAML with one section per BIOL-1 module.

    Parameters
    ----------
    course_dir:
        Path to ``course_development/biol-1/course/`` containing ``module-*/`` dirs.
    output_dir:
        Directory where PNG assets and the YAML file will be written.
    lecturecreate_config_path:
        Optional path to a LectureCreate render config YAML.

    Returns
    -------
    str
        The generated combined YAML string.
    """
    course = Path(course_dir)
    modules = sorted(
        p for p in course.glob("module-*") if p.is_dir() and (p / "module.toml").exists()
    )

    lines: list[str] = []
    _emit = lines.append

    _emit("# Generated from course_development/biol-1/course — do not hand-edit")
    _emit('title: "BIOL-1: General Biology — Full Course"')
    _emit('subtitle: "College of the Redwoods — Pelican Bay"')
    _emit("width: 1920")
    _emit("height: 1080")
    _emit("fps: 30")
    _emit("")
    _emit("metadata:")
    _emit('  author: "Dr. Daniel Ari Friedman"')
    _emit('  topic: "General Biology"')
    _emit('  series: "BIOL-1: General Biology"')
    _emit("  series_index: 0")
    _emit(f"  series_total: {len(modules)}")
    _emit("")

    _emit("sections:")
    for mod in modules:
        # Reuse per-module YAML generation via the existing builder,
        # then extract the section block to avoid duplication.
        module_yaml = build_module_lecture_yaml(mod, output_dir, lecturecreate_config_path)
        section_start = module_yaml.find("sections:")
        if section_start == -1:
            continue
        section_body = module_yaml[section_start + len("sections:") :].strip()
        _emit(section_body)
        _emit("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Rendering via subprocess
# ---------------------------------------------------------------------------


def render_module_video(
    yaml_path: Path | str,
    output_dir: Path | str,
    config_path: Path | str | None = None,
    lecturecreate_bin: str | None = None,
    qr: bool = False,
    backend: str = "system",
) -> subprocess.CompletedProcess[str]:
    """Invoke LectureCreate to render a YAML manifest to video.

    Parameters
    ----------
    yaml_path:
        Path to the generated lecture YAML file.
    output_dir:
        Directory for rendered outputs (video, captions, manifest).
    config_path:
        Optional path to a LectureCreate render config.
    lecturecreate_bin:
        Path to the lecturecreate executable; defaults to ``lecturecreate``.
    qr:
        If True, pass ``--qr`` to add per-slide QR codes linking to source.
    backend:
        TTS backend name (e.g. ``system``, ``edge``). Default ``system``.

    Returns
    -------
    subprocess.CompletedProcess[str]
        The completed subprocess result.
    """
    bin_path = lecturecreate_bin or LECTURECREATE_BIN
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    cmd = [
        bin_path,
        "from-yaml",
        str(yaml_path),
        "--backend",
        backend,
        "--out",
        str(out),
    ]
    if qr:
        cmd.append("--qr")
    if config_path:
        # LectureCreate runs with ``cwd=out`` so relative config paths would
        # resolve against a generated artifact directory instead of the repo.
        cmd.extend(["--config", str(Path(config_path).expanduser().resolve())])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(out),
        check=False,
    )
    if result.returncode == 0:
        _relativize_render_metadata(out)
    return result


def _relativize_render_metadata(output_dir: Path) -> None:
    """Make LectureCreate JSON/manifests portable after a successful render."""
    root = output_dir.resolve()

    def convert(value: object) -> object:
        if isinstance(value, dict):
            return {key: convert(item) for key, item in value.items()}
        if isinstance(value, list):
            return [convert(item) for item in value]
        if isinstance(value, str) and value.startswith("/"):
            candidate = Path(value).resolve(strict=False)
            try:
                return candidate.relative_to(root).as_posix()
            except ValueError:
                return value
        return value

    for path in (
        output_dir / output_dir.name / "lectures" / "lecture.json",
        output_dir / output_dir.name / "manifests" / "render_manifest.json",
    ):
        if not path.is_file():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        path.write_text(json.dumps(convert(payload), indent=2) + "\n", encoding="utf-8")
