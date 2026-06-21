"""Typed BIOL-1 module content loading, validation, and rendering."""

from __future__ import annotations

import html
import math
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ModuleContentError(ValueError):
    """Raised when a module manifest is missing or invalid."""


@dataclass(frozen=True)
class Term:
    name: str
    definition: str


@dataclass(frozen=True)
class QuizQuestion:
    question: str
    options: tuple[str, str, str, str]
    answer: str
    explanation: str


@dataclass(frozen=True)
class ModuleAsset:
    path: str
    kind: str
    description: str


@dataclass(frozen=True)
class VisualNode:
    id: str
    label: str
    detail: str
    cluster: str = "Core"


@dataclass(frozen=True)
class VisualEdge:
    source: str
    target: str
    label: str


@dataclass(frozen=True)
class ProcessStage:
    label: str
    detail: str


@dataclass(frozen=True)
class RetrievalPrompt:
    prompt: str
    check: str


@dataclass(frozen=True)
class ConceptMapSpec:
    central_claim: str
    nodes: tuple[VisualNode, ...]
    edges: tuple[VisualEdge, ...]
    clusters: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProcessModelSpec:
    stages: tuple[ProcessStage, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    feedbacks: tuple[str, ...]
    constraints: tuple[str, ...] = ()


@dataclass(frozen=True)
class RetrievalCardSpec:
    prompts: tuple[RetrievalPrompt, ...]
    terms: tuple[str, ...]
    lab_connection: str


@dataclass(frozen=True)
class GeneratedImage:
    id: str
    title: str
    kind: str
    output: str
    prompt: str = ""
    concept_map: ConceptMapSpec | None = None
    process_model: ProcessModelSpec | None = None
    retrieval_card: RetrievalCardSpec | None = None


GENERATED_IMAGE_KINDS = {"concept-map", "process-model", "retrieval-card"}
REQUIRED_IMAGE_IDS = {"concept-map", "process-model", "retrieval-card"}
SVG_WIDTH = 1200
SVG_HEIGHT = 720


@dataclass(frozen=True)
class ModuleContent:
    module_dir: Path
    number: int
    slug: str
    title: str
    lab: str
    topics: tuple[str, ...]
    contents: tuple[str, ...]
    learning_objectives: tuple[str, ...]
    terms: tuple[Term, ...]
    study_tips: tuple[str, ...]
    learning_questions: tuple[str, ...]
    practice_quiz: tuple[QuizQuestion, ...]
    assets: tuple[ModuleAsset, ...] = field(default_factory=tuple)
    generated_images: tuple[GeneratedImage, ...] = field(default_factory=tuple)


def load_module_content(module_dir: Path | str) -> ModuleContent:
    """Load and validate a module manifest from ``module.toml``."""
    directory = Path(module_dir)
    manifest = directory / "module.toml"
    if not manifest.exists():
        raise ModuleContentError(f"Missing module manifest: {manifest}")
    try:
        with manifest.open("rb") as handle:
            raw = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise ModuleContentError(f"Malformed module.toml in {directory}: {exc}") from exc

    module_data = _table(raw, "module", manifest)
    content = ModuleContent(
        module_dir=directory,
        number=_int(module_data, "number", manifest),
        slug=_str(module_data, "slug", manifest),
        title=_str(module_data, "title", manifest),
        lab=_str(module_data, "lab", manifest),
        topics=tuple(_str_list(module_data, "topics", manifest)),
        contents=tuple(_str_list(module_data, "contents", manifest)),
        learning_objectives=tuple(_str_list(module_data, "learning_objectives", manifest)),
        terms=tuple(
            Term(name=_str(item, "name", manifest), definition=_str(item, "definition", manifest))
            for item in _array(raw, "terms", manifest)
        ),
        study_tips=tuple(_str_list(module_data, "study_tips", manifest)),
        learning_questions=tuple(_str_list(module_data, "learning_questions", manifest)),
        practice_quiz=tuple(_quiz_question(item, manifest) for item in _array(raw, "practice_quiz", manifest)),
        assets=tuple(
            ModuleAsset(
                path=_str(item, "path", manifest),
                kind=_str(item, "kind", manifest),
                description=_str(item, "description", manifest),
            )
            for item in raw.get("assets", [])
        ),
        generated_images=tuple(_generated_image(item, manifest) for item in raw.get("generated_images", [])),
    )
    issues = validate_module_content(content, directory)
    if issues:
        raise ModuleContentError("; ".join(issues))
    return content


def validate_module_content(module: ModuleContent, module_dir: Path | None = None) -> list[str]:
    """Return validation issues for a loaded module manifest."""
    directory = module_dir or module.module_dir
    issues: list[str] = []
    expected_prefix = f"module-{module.number:02d}-"
    if not module.slug.startswith(expected_prefix):
        issues.append(f"{module.slug} must start with {expected_prefix}")
    if directory.name != module.slug:
        issues.append(f"manifest slug {module.slug} does not match directory {directory.name}")
    for label, values, minimum in (
        ("topics", module.topics, 2),
        ("contents", module.contents, 2),
        ("learning_objectives", module.learning_objectives, 3),
        ("terms", module.terms, 3),
        ("learning_questions", module.learning_questions, 8),
        ("practice_quiz", module.practice_quiz, 4),
    ):
        if len(values) < minimum:
            issues.append(f"{module.slug} has {len(values)} {label}; expected at least {minimum}")
    if module.lab and not re.match(r"^lab-\d{2}_[a-z0-9-]+\.md$", module.lab):
        issues.append(f"{module.slug} lab reference is malformed: {module.lab}")
    for quiz in module.practice_quiz:
        if quiz.answer not in {"A", "B", "C", "D"}:
            issues.append(f"{module.slug} quiz answer must be A-D: {quiz.question}")
        if len(quiz.options) != 4:
            issues.append(f"{module.slug} quiz question must have exactly 4 options: {quiz.question}")
    answers = [quiz.answer for quiz in module.practice_quiz]
    if len(answers) >= 4 and set(answers[:4]) != {"A", "B", "C", "D"}:
        issues.append(f"{module.slug} first four practice quiz answers must balance A-D")
    for asset in module.assets:
        asset_path = (directory / asset.path).resolve()
        try:
            asset_path.relative_to(directory.resolve())
        except ValueError:
            issues.append(f"{module.slug} asset escapes module directory: {asset.path}")
        if not asset_path.exists():
            issues.append(f"{module.slug} asset does not exist: {asset.path}")
    issues.extend(_validate_generated_images(module, directory))
    return issues


def render_module_materials(module_dir: Path | str, dry_run: bool = False) -> dict[str, object]:
    """Render generated student materials for one module."""
    module = load_module_content(module_dir)
    outputs = [
        module.module_dir / "keys-to-success.md",
        module.module_dir / "questions.md",
        module.module_dir / "practice-quiz.md",
    ]
    outputs.extend(module.module_dir / image.output for image in module.generated_images)
    outputs.extend(
        [
            module.module_dir / "resources" / "README.md",
            module.module_dir / "resources" / "AGENTS.md",
            module.module_dir / "resources" / "generated" / "README.md",
            module.module_dir / "resources" / "generated" / "AGENTS.md",
            module.module_dir / "resources" / "generated" / "asset-index.md",
        ]
    )
    if dry_run:
        return {"module": module.slug, "outputs": [str(path) for path in outputs], "written": 0}

    (module.module_dir / "resources" / "generated").mkdir(parents=True, exist_ok=True)
    (module.module_dir / "keys-to-success.md").write_text(_render_keys(module), encoding="utf-8")
    (module.module_dir / "questions.md").write_text(_render_questions(module), encoding="utf-8")
    (module.module_dir / "practice-quiz.md").write_text(_render_quiz(module), encoding="utf-8")
    for image in module.generated_images:
        output_path = module.module_dir / image.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(_render_svg(module, image), encoding="utf-8")
    resources_dir = module.module_dir / "resources"
    if not resources_dir.joinpath("README.md").exists():
        resources_dir.joinpath("README.md").write_text(_render_resources_readme(module), encoding="utf-8")
    if not resources_dir.joinpath("AGENTS.md").exists():
        resources_dir.joinpath("AGENTS.md").write_text(_render_resources_agents(module), encoding="utf-8")
    generated_dir = module.module_dir / "resources" / "generated"
    generated_dir.joinpath("README.md").write_text(_render_generated_readme(module), encoding="utf-8")
    generated_dir.joinpath("AGENTS.md").write_text(_render_generated_agents(module), encoding="utf-8")
    generated_dir.joinpath("asset-index.md").write_text(_render_asset_index(module), encoding="utf-8")
    return {"module": module.slug, "outputs": [str(path) for path in outputs], "written": len(outputs)}


def render_course_module_materials(
    course_root: Path | str,
    module_filter: int | None = None,
    dry_run: bool = False,
) -> dict[str, object]:
    """Render structured materials for every module under a BIOL-1 course root."""
    course_path = Path(course_root)
    modules = _module_dirs(course_path, module_filter)
    results = [render_module_materials(module_dir, dry_run=dry_run) for module_dir in modules]
    written = sum(
        value
        for result in results
        for value in [result.get("written")]
        if isinstance(value, int)
    )
    return {
        "course": str(course_path),
        "modules": results,
        "module_count": len(results),
        "written": written,
    }


def describe_course_module_materials(course_root: Path | str, module_filter: int | None = None) -> str:
    """Return a dry-run report for structured module material generation."""
    course_path = Path(course_root)
    lines = ["Structured module materials:"]
    for module_dir in _module_dirs(course_path, module_filter):
        module = load_module_content(module_dir)
        lines.append(
            f"  {module.slug}: {len(module.learning_objectives)} objectives, "
            f"{len(module.terms)} terms, {len(module.learning_questions)} questions, "
            f"{len(module.practice_quiz)} quiz items"
        )
    return "\n".join(lines)


def _module_dirs(course_root: Path, module_filter: int | None) -> list[Path]:
    course_dir = course_root / "course"
    modules = sorted(path for path in course_dir.glob("module-*") if path.is_dir())
    if module_filter is not None:
        modules = [path for path in modules if re.match(rf"module-0*{module_filter}\b", path.name)]
    return modules


def _render_keys(module: ModuleContent) -> str:
    lines = [_generated_notice(), f"# Module {module.number}: {module.title} - Keys to Success", ""]
    lines.extend(["## Learning Objectives", "", "By the end of this module, you should be able to:", ""])
    lines.extend(f"{idx}. {objective}" for idx, objective in enumerate(module.learning_objectives, 1))
    lines.extend(["", "## Topics", ""])
    lines.extend(f"- {topic}" for topic in module.topics)
    lines.extend(["", "## Key Terms to Know", ""])
    lines.extend(f"- **{term.name}** - {term.definition}" for term in module.terms)
    lines.extend(["", "## Core Contents", ""])
    lines.extend(f"{idx}. {content}" for idx, content in enumerate(module.contents, 1))
    if module.study_tips:
        lines.extend(["", "## Study Tips", ""])
        lines.extend(f"{idx}. {tip}" for idx, tip in enumerate(module.study_tips, 1))
    if module.lab:
        lines.extend(["", "## Connected Lab", "", f"- `{module.lab}`"])
    if module.generated_images:
        lines.extend(["", "## Generated Visuals", ""])
        lines.extend(f"- [{image.title}]({image.output})" for image in module.generated_images)
    return "\n".join(lines).rstrip() + "\n"


def _render_questions(module: ModuleContent) -> str:
    lines = [_generated_notice(), f"# Module {module.number}: {module.title} - Learning Questions", ""]
    lines.extend(f"{idx}. {question}" for idx, question in enumerate(module.learning_questions, 1))
    return "\n\n".join(lines).rstrip() + "\n"


def _render_quiz(module: ModuleContent) -> str:
    lines = [_generated_notice(), f"# Module {module.number}: {module.title} - Practice Quiz", ""]
    lines.append("Use this low-stakes quiz after reviewing the module keys and learning questions.")
    lines.append("")
    for idx, quiz in enumerate(module.practice_quiz, 1):
        lines.append(f"{idx}. {quiz.question}")
        for letter, option in zip(("A", "B", "C", "D"), quiz.options):
            lines.append(f"   - {letter}. {option}")
        lines.append(f"   - Answer: {quiz.answer}")
        lines.append(f"   - Why: {quiz.explanation}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_asset_index(module: ModuleContent) -> str:
    lines = [_generated_notice(), f"# Module {module.number}: {module.title} - Generated Asset Index", ""]
    lines.append("## Deterministic Generated Assets")
    lines.append("")
    for image in module.generated_images:
        lines.append(f"- **{image.title}** (`{image.output}`) - {image.kind}")
        purpose = _visual_purpose(image)
        if purpose:
            lines.append(f"  - Purpose: {purpose}")
        if image.prompt:
            lines.append(f"  - Prompt metadata: {image.prompt}")
    if module.assets:
        lines.extend(["", "## Module-Local Assets", ""])
        lines.extend(f"- `{asset.path}` ({asset.kind}) - {asset.description}" for asset in module.assets)
    return "\n".join(lines).rstrip() + "\n"


def _render_generated_readme(module: ModuleContent) -> str:
    return (
        f"# Module {module.number} Generated Assets\n\n"
        "This directory is generated from the module's `module.toml`. "
        "Do not edit generated SVG files by hand; update the manifest and rerun "
        "`software/scripts/generate_module_materials.py`.\n"
    )


def _render_resources_readme(module: ModuleContent) -> str:
    return (
        f"# Module {module.number} Resources\n\n"
        "Module-local resource directory. Deterministic generated visual assets are "
        "stored under `generated/` and are produced from `../module.toml`.\n"
    )


def _render_resources_agents(module: ModuleContent) -> str:
    return (
        f"# Technical Documentation: Module {module.number} Resources\n\n"
        "Resource directory for the BIOL-1 structured module-content pipeline. "
        "Keep hand-authored assets documented here; generated assets live in `generated/`.\n"
    )


def _render_generated_agents(module: ModuleContent) -> str:
    return (
        f"# Technical Documentation: Module {module.number} Generated Assets\n\n"
        "Generated deterministic SVG assets and asset index for the BIOL-1 structured "
        "module-content pipeline. Source of truth: `../../module.toml`.\n"
    )


def _render_svg(module: ModuleContent, image: GeneratedImage) -> str:
    if image.kind == "concept-map":
        return _render_concept_map_svg(module, image)
    if image.kind == "process-model":
        return _render_process_model_svg(module, image)
    if image.kind == "retrieval-card":
        return _render_retrieval_card_svg(module, image)
    raise ModuleContentError(f"Unsupported generated image kind: {image.kind}")


def _render_concept_map_svg(module: ModuleContent, image: GeneratedImage) -> str:
    if image.concept_map is None:
        raise ModuleContentError(f"{module.slug} concept-map visual payload is missing")
    spec = image.concept_map
    title = html.escape(image.title)
    desc = html.escape(f"Concept map for Module {module.number}: {module.title}. {spec.central_claim}")
    palette = _module_palette(module.number)
    positions = _radial_positions(len(spec.nodes), 600, 365, 360, 190)
    position_by_id = {node.id: positions[idx] for idx, node in enumerate(spec.nodes)}
    edges = []
    for edge in spec.edges:
        x1, y1 = position_by_id[edge.source]
        x2, y2 = position_by_id[edge.target]
        edges.append(
            f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" class="edge" />'
            f'<text x="{(x1 + x2) / 2:.1f}" y="{(y1 + y2) / 2:.1f}" '
            f'class="edge-label">{html.escape(edge.label)}</text>'
        )
    nodes = []
    for idx, node in enumerate(spec.nodes):
        x, y = positions[idx]
        nodes.append(
            f'<g class="node-group"><rect x="{x - 120:.1f}" y="{y - 48:.1f}" '
            f'width="240" height="96" rx="22" class="node" />'
            f'{_svg_wrapped_text(node.label, x, y - 12, 21, 20, "node-label", anchor="middle")}'
            f'{_svg_wrapped_text(node.detail, x, y + 22, 27, 14, "node-detail", anchor="middle", max_lines=2)}'
            f'</g>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" aria-label="{title}">
  <title>{title}</title>
  <desc>{desc}</desc>
  <style>{_svg_style(palette)}</style>
  <defs>{_svg_defs(palette)}</defs>
  <rect class="bg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" />
  <path class="halo" d="M80 100 C260 20 458 88 610 62 C848 20 1052 74 1148 214 L1148 656 L52 656 L52 178 C64 142 70 118 80 100 Z" />
  <text x="70" y="72" class="eyebrow">Module {module.number:02d} / Concept Map</text>
  <text x="70" y="118" class="title-text">{title}</text>
  <rect x="330" y="282" width="540" height="166" rx="34" class="claim-card" />
  <text x="600" y="322" class="claim-kicker">Central claim</text>
  {_svg_wrapped_text(spec.central_claim, 600, 366, 48, 25, "claim-text", anchor="middle", max_lines=3)}
  {''.join(edges)}
  {''.join(nodes)}
  <text x="70" y="672" class="footer">Linked lab: {html.escape(module.lab)} / Generated from explicit module.toml visual schema</text>
</svg>
'''


def _render_process_model_svg(module: ModuleContent, image: GeneratedImage) -> str:
    if image.process_model is None:
        raise ModuleContentError(f"{module.slug} process-model visual payload is missing")
    spec = image.process_model
    title = html.escape(image.title)
    desc = html.escape(f"Process model for Module {module.number}: {module.title}.")
    palette = _module_palette(module.number)
    count = len(spec.stages)
    x_values = [160 + idx * (880 / max(count - 1, 1)) for idx in range(count)]
    stages = []
    arrows = []
    for idx, stage in enumerate(spec.stages):
        x = x_values[idx]
        y = 330 if idx % 2 == 0 else 405
        stages.append(
            f'<g><circle cx="{x:.1f}" cy="{y:.1f}" r="70" class="stage" />'
            f'<text x="{x:.1f}" y="{y - 82:.1f}" class="stage-num">{idx + 1:02d}</text>'
            f'{_svg_wrapped_text(stage.label, x, y - 16, 19, 18, "stage-label", anchor="middle", max_lines=2)}'
            f'{_svg_wrapped_text(stage.detail, x, y + 28, 22, 13, "stage-detail", anchor="middle", max_lines=2)}'
            f'</g>'
        )
        if idx < count - 1:
            arrows.append(
                f'<path d="M {x + 78:.1f} {y:.1f} C {x + 118:.1f} {y - 42:.1f}, '
                f'{x_values[idx + 1] - 118:.1f} {395 if y == 330 else 340:.1f}, '
                f'{x_values[idx + 1] - 78:.1f} {405 if y == 330 else 330:.1f}" class="arrow" />'
            )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" aria-label="{title}">
  <title>{title}</title>
  <desc>{desc}</desc>
  <style>{_svg_style(palette)}</style>
  <defs>{_svg_defs(palette)}</defs>
  <rect class="bg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" />
  <rect x="48" y="48" width="1104" height="624" rx="42" class="frame" />
  <text x="84" y="100" class="eyebrow">Module {module.number:02d} / Process Model</text>
  <text x="84" y="148" class="title-text">{title}</text>
  <rect x="84" y="182" width="318" height="92" rx="24" class="side-card" />
  <text x="110" y="216" class="card-kicker">Inputs</text>
  {_svg_bullets(spec.inputs, 110, 244, 30, 15, "mini-text", max_items=3)}
  <rect x="798" y="182" width="318" height="92" rx="24" class="side-card" />
  <text x="824" y="216" class="card-kicker">Outputs</text>
  {_svg_bullets(spec.outputs, 824, 244, 30, 15, "mini-text", max_items=3)}
  {''.join(arrows)}
  {''.join(stages)}
  <rect x="84" y="562" width="1032" height="70" rx="22" class="feedback-card" />
  <text x="112" y="590" class="card-kicker">Feedbacks and constraints</text>
  {_svg_wrapped_text('; '.join((*spec.feedbacks, *spec.constraints)), 112, 618, 116, 16, "mini-text", max_lines=2)}
  <text x="84" y="668" class="footer">Linked lab: {html.escape(module.lab)}</text>
</svg>
'''


def _render_retrieval_card_svg(module: ModuleContent, image: GeneratedImage) -> str:
    if image.retrieval_card is None:
        raise ModuleContentError(f"{module.slug} retrieval-card visual payload is missing")
    spec = image.retrieval_card
    title = html.escape(image.title)
    desc = html.escape(f"Retrieval card for Module {module.number}: {module.title}.")
    palette = _module_palette(module.number)
    prompt_cards = []
    for idx, prompt in enumerate(spec.prompts[:4]):
        x = 92 + (idx % 2) * 512
        y = 190 + (idx // 2) * 170
        prompt_cards.append(
            f'<rect x="{x}" y="{y}" width="462" height="132" rx="26" class="prompt-card" />'
            f'<text x="{x + 28}" y="{y + 38}" class="stage-num">Q{idx + 1}</text>'
            f'{_svg_wrapped_text(prompt.prompt, x + 28, y + 66, 45, 17, "prompt-text", max_lines=2)}'
            f'{_svg_wrapped_text("Check: " + prompt.check, x + 28, y + 112, 52, 13, "check-text", max_lines=1)}'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" aria-label="{title}">
  <title>{title}</title>
  <desc>{desc}</desc>
  <style>{_svg_style(palette)}</style>
  <defs>{_svg_defs(palette)}</defs>
  <rect class="bg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" />
  <path class="halo" d="M44 72 H1156 V648 H44 Z" />
  <text x="82" y="92" class="eyebrow">Module {module.number:02d} / Retrieval Card</text>
  <text x="82" y="142" class="title-text">{title}</text>
  {''.join(prompt_cards)}
  <rect x="92" y="548" width="462" height="86" rx="24" class="side-card" />
  <text x="120" y="582" class="card-kicker">Terms to use</text>
  {_svg_wrapped_text(', '.join(spec.terms), 120, 612, 54, 17, "mini-text", max_lines=2)}
  <rect x="604" y="548" width="504" height="86" rx="24" class="side-card" />
  <text x="632" y="582" class="card-kicker">Lab connection</text>
  {_svg_wrapped_text(spec.lab_connection, 632, 612, 58, 17, "mini-text", max_lines=2)}
  <text x="82" y="672" class="footer">Cover notes, answer aloud, check evidence, then revise.</text>
</svg>
'''


def _generated_notice() -> str:
    return "<!-- Generated from module.toml; edit the manifest, not this file. -->"


def _quiz_question(item: dict[str, Any], manifest: Path) -> QuizQuestion:
    options = tuple(_str_list(item, "options", manifest))
    if len(options) != 4:
        raise ModuleContentError(f"{manifest}: practice quiz options must contain exactly 4 values")
    return QuizQuestion(
        question=_str(item, "question", manifest),
        options=(options[0], options[1], options[2], options[3]),
        answer=_str(item, "answer", manifest).upper(),
        explanation=_str(item, "explanation", manifest),
    )


def _generated_image(item: dict[str, Any], manifest: Path) -> GeneratedImage:
    kind = _str(item, "kind", manifest)
    image = GeneratedImage(
        id=_str(item, "id", manifest),
        title=_str(item, "title", manifest),
        kind=kind,
        output=_str(item, "output", manifest),
        prompt=str(item.get("prompt", "")).strip(),
        concept_map=_concept_map_spec(item, manifest) if kind == "concept-map" else None,
        process_model=_process_model_spec(item, manifest) if kind == "process-model" else None,
        retrieval_card=_retrieval_card_spec(item, manifest) if kind == "retrieval-card" else None,
    )
    return image


def _concept_map_spec(item: dict[str, Any], manifest: Path) -> ConceptMapSpec:
    return ConceptMapSpec(
        central_claim=_str(item, "central_claim", manifest),
        nodes=tuple(
            VisualNode(
                id=_str(node, "id", manifest),
                label=_str(node, "label", manifest),
                detail=_str(node, "detail", manifest),
                cluster=str(node.get("cluster", "Core")).strip() or "Core",
            )
            for node in _array_from(item, "nodes", manifest)
        ),
        edges=tuple(
            VisualEdge(
                source=_str(edge, "source", manifest),
                target=_str(edge, "target", manifest),
                label=_str(edge, "label", manifest),
            )
            for edge in _array_from(item, "edges", manifest)
        ),
        clusters=tuple(_optional_str_list(item, "clusters", manifest)),
    )


def _process_model_spec(item: dict[str, Any], manifest: Path) -> ProcessModelSpec:
    return ProcessModelSpec(
        stages=tuple(
            ProcessStage(label=_str(stage, "label", manifest), detail=_str(stage, "detail", manifest))
            for stage in _array_from(item, "stages", manifest)
        ),
        inputs=tuple(_str_list(item, "inputs", manifest)),
        outputs=tuple(_str_list(item, "outputs", manifest)),
        feedbacks=tuple(_str_list(item, "feedbacks", manifest)),
        constraints=tuple(_optional_str_list(item, "constraints", manifest)),
    )


def _retrieval_card_spec(item: dict[str, Any], manifest: Path) -> RetrievalCardSpec:
    return RetrievalCardSpec(
        prompts=tuple(
            RetrievalPrompt(prompt=_str(prompt, "prompt", manifest), check=_str(prompt, "check", manifest))
            for prompt in _array_from(item, "prompts", manifest)
        ),
        terms=tuple(_str_list(item, "terms", manifest)),
        lab_connection=_str(item, "lab_connection", manifest),
    )


def _validate_generated_images(module: ModuleContent, directory: Path) -> list[str]:
    issues: list[str] = []
    ids = [image.id for image in module.generated_images]
    outputs = [image.output for image in module.generated_images]
    if set(ids) != REQUIRED_IMAGE_IDS or len(ids) != len(REQUIRED_IMAGE_IDS):
        issues.append(
            f"{module.slug} generated images must be exactly: "
            f"{', '.join(sorted(REQUIRED_IMAGE_IDS))}"
        )
    if len(ids) != len(set(ids)):
        issues.append(f"{module.slug} generated image ids must be unique")
    if len(outputs) != len(set(outputs)):
        issues.append(f"{module.slug} generated image outputs must be unique")
    for image in module.generated_images:
        output_path = (directory / image.output).resolve()
        expected_output = f"resources/generated/module-{module.number:02d}-{image.kind}.svg"
        try:
            output_path.relative_to(directory.resolve())
        except ValueError:
            issues.append(f"{module.slug} generated image escapes module directory: {image.output}")
        if not image.output.startswith("resources/generated/"):
            issues.append(f"{module.slug} generated image must live in resources/generated/: {image.output}")
        if image.output != expected_output:
            issues.append(f"{module.slug} generated image output is {image.output}; expected {expected_output}")
        if output_path.suffix.lower() != ".svg":
            issues.append(f"{module.slug} generated image must be SVG: {image.output}")
        if image.kind not in GENERATED_IMAGE_KINDS:
            issues.append(f"{module.slug} generated image kind is unsupported: {image.kind}")
            continue
        issues.extend(_validate_generated_image_payload(module, image))
    return issues


def _validate_generated_image_payload(module: ModuleContent, image: GeneratedImage) -> list[str]:
    issues: list[str] = []
    if image.kind == "concept-map":
        concept_spec = image.concept_map
        if concept_spec is None:
            return [f"{module.slug} concept-map visual payload is missing"]
        if len(concept_spec.nodes) < 3:
            issues.append(f"{module.slug} concept-map needs at least 3 nodes")
        node_ids = [node.id for node in concept_spec.nodes]
        if len(node_ids) != len(set(node_ids)):
            issues.append(f"{module.slug} concept-map node ids must be unique")
        for node in concept_spec.nodes:
            if len(node.label) > 80 or len(node.detail) > 120:
                issues.append(f"{module.slug} concept-map label/detail is too long for wrapped SVG text")
        for edge in concept_spec.edges:
            if edge.source not in node_ids or edge.target not in node_ids:
                issues.append(f"{module.slug} concept-map has dangling edge: {edge.source}->{edge.target}")
    elif image.kind == "process-model":
        process_spec = image.process_model
        if process_spec is None:
            return [f"{module.slug} process-model visual payload is missing"]
        if len(process_spec.stages) < 3:
            issues.append(f"{module.slug} process-model needs at least 3 stages")
        if not process_spec.inputs or not process_spec.outputs or not process_spec.feedbacks:
            issues.append(f"{module.slug} process-model needs inputs, outputs, and feedbacks")
        for stage in process_spec.stages:
            if len(stage.label) > 70 or len(stage.detail) > 120:
                issues.append(f"{module.slug} process-model stage text is too long for wrapped SVG text")
    elif image.kind == "retrieval-card":
        retrieval_spec = image.retrieval_card
        if retrieval_spec is None:
            return [f"{module.slug} retrieval-card visual payload is missing"]
        if len(retrieval_spec.prompts) < 4:
            issues.append(f"{module.slug} retrieval-card needs at least 4 prompts")
        if len(retrieval_spec.terms) < 3:
            issues.append(f"{module.slug} retrieval-card needs at least 3 terms")
        for prompt in retrieval_spec.prompts:
            if len(prompt.prompt) > 130 or len(prompt.check) > 120:
                issues.append(f"{module.slug} retrieval-card prompt/check is too long for wrapped SVG text")
    return issues


def _visual_purpose(image: GeneratedImage) -> str:
    if image.concept_map is not None:
        return image.concept_map.central_claim
    if image.process_model is not None:
        return " -> ".join(stage.label for stage in image.process_model.stages[:4])
    if image.retrieval_card is not None:
        return image.retrieval_card.lab_connection
    return ""


def _module_palette(module_number: int) -> dict[str, str]:
    palettes = [
        {"bg": "#f7efe2", "ink": "#1f2a24", "muted": "#59685f", "accent": "#c45f35", "accent2": "#245f73", "panel": "#fffaf0"},
        {"bg": "#ecf4f2", "ink": "#172d35", "muted": "#4f6670", "accent": "#1f7a6d", "accent2": "#b55f24", "panel": "#fbfffd"},
        {"bg": "#f2edf7", "ink": "#281d34", "muted": "#685d72", "accent": "#7b4f9d", "accent2": "#b36b2c", "panel": "#fffafd"},
        {"bg": "#f4f1e6", "ink": "#2c2517", "muted": "#6a614d", "accent": "#9b3f2f", "accent2": "#2f6f4e", "panel": "#fffdf5"},
    ]
    return palettes[(module_number - 1) % len(palettes)]


def _svg_style(palette: dict[str, str]) -> str:
    return f'''
    .bg {{ fill: {palette["bg"]}; }}
    .halo {{ fill: url(#wash); opacity: 0.92; }}
    .frame {{ fill: {palette["panel"]}; stroke: {palette["ink"]}; stroke-width: 3; }}
    .eyebrow {{ fill: {palette["accent"]}; font: 800 18px Georgia, serif; letter-spacing: 1.5px; text-transform: uppercase; }}
    .title-text {{ fill: {palette["ink"]}; font: 800 38px Georgia, serif; }}
    .footer {{ fill: {palette["muted"]}; font: 16px Georgia, serif; }}
    .claim-card, .side-card, .feedback-card, .prompt-card {{ fill: {palette["panel"]}; stroke: {palette["ink"]}; stroke-width: 2.5; filter: url(#shadow); }}
    .claim-kicker, .card-kicker {{ fill: {palette["accent"]}; font: 800 17px Georgia, serif; letter-spacing: 0.8px; text-transform: uppercase; }}
    .claim-text {{ fill: {palette["ink"]}; font: 700 25px Georgia, serif; }}
    .node {{ fill: {palette["panel"]}; stroke: {palette["accent2"]}; stroke-width: 3; filter: url(#shadow); }}
    .node-label {{ fill: {palette["ink"]}; font: 800 20px Georgia, serif; }}
    .node-detail {{ fill: {palette["muted"]}; font: 14px Georgia, serif; }}
    .edge {{ stroke: {palette["accent"]}; stroke-width: 4; stroke-linecap: round; opacity: 0.72; }}
    .edge-label {{ fill: {palette["accent"]}; font: 700 13px Georgia, serif; text-anchor: middle; paint-order: stroke; stroke: {palette["bg"]}; stroke-width: 4; }}
    .stage {{ fill: {palette["panel"]}; stroke: {palette["accent"]}; stroke-width: 5; filter: url(#shadow); }}
    .stage-num {{ fill: {palette["accent2"]}; font: 900 18px Georgia, serif; }}
    .stage-label {{ fill: {palette["ink"]}; font: 800 18px Georgia, serif; }}
    .stage-detail, .mini-text, .check-text {{ fill: {palette["muted"]}; font: 15px Georgia, serif; }}
    .arrow {{ fill: none; stroke: {palette["accent2"]}; stroke-width: 5; stroke-linecap: round; marker-end: url(#arrowhead); }}
    .prompt-text {{ fill: {palette["ink"]}; font: 700 17px Georgia, serif; }}
    .palette-high-design {{ fill: {palette["accent"]}; }}
    @media print {{ .claim-card, .side-card, .feedback-card, .prompt-card, .node, .stage {{ filter: none; }} }}
    '''


def _svg_defs(palette: dict[str, str]) -> str:
    return f'''
    <linearGradient id="wash" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="{palette["panel"]}" />
      <stop offset="1" stop-color="{palette["accent2"]}" stop-opacity="0.18" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="7" flood-color="{palette["ink"]}" flood-opacity="0.16"/>
    </filter>
    <marker id="arrowhead" markerWidth="12" markerHeight="8" refX="11" refY="4" orient="auto">
      <polygon points="0 0, 12 4, 0 8" fill="{palette["accent2"]}" />
    </marker>
    '''


def _radial_positions(count: int, cx: float, cy: float, rx: float, ry: float) -> list[tuple[float, float]]:
    return [
        (
            cx + math.cos(-math.pi / 2 + 2 * math.pi * idx / count) * rx,
            cy + math.sin(-math.pi / 2 + 2 * math.pi * idx / count) * ry,
        )
        for idx in range(count)
    ]


def _wrap_text(text: str, max_chars: int, max_lines: int | None = None) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    if max_lines is not None and len(lines) > max_lines:
        kept = lines[:max_lines]
        kept[-1] = kept[-1].rstrip(".,;:") + "..."
        return kept
    return lines or [""]


def _svg_wrapped_text(
    text: str,
    x: float,
    y: float,
    max_chars: int,
    line_height: int,
    css_class: str,
    *,
    anchor: str = "start",
    max_lines: int | None = None,
) -> str:
    anchor_attr = f' text-anchor="{anchor}"' if anchor != "start" else ""
    lines = _wrap_text(text, max_chars, max_lines)
    tspans = "".join(
        f'<tspan x="{x:.1f}" dy="{0 if idx == 0 else line_height}">{html.escape(line)}</tspan>'
        for idx, line in enumerate(lines)
    )
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{css_class}"{anchor_attr}>{tspans}</text>'


def _svg_bullets(
    items: tuple[str, ...],
    x: float,
    y: float,
    max_chars: int,
    line_height: int,
    css_class: str,
    *,
    max_items: int,
) -> str:
    lines = []
    for idx, item in enumerate(items[:max_items]):
        lines.append(_svg_wrapped_text(f"• {item}", x, y + idx * line_height, max_chars, line_height, css_class))
    return "".join(lines)


def _table(raw: dict[str, Any], key: str, manifest: Path) -> dict[str, Any]:
    value = raw.get(key)
    if not isinstance(value, dict):
        raise ModuleContentError(f"{manifest}: missing [{key}] table")
    return value


def _array(raw: dict[str, Any], key: str, manifest: Path) -> list[dict[str, Any]]:
    value = raw.get(key)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ModuleContentError(f"{manifest}: missing [[{key}]] entries")
    return value


def _array_from(raw: dict[str, Any], key: str, manifest: Path) -> list[dict[str, Any]]:
    value = raw.get(key)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ModuleContentError(f"{manifest}: missing [[generated_images.{key}]] entries")
    return value


def _str(raw: dict[str, Any], key: str, manifest: Path) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ModuleContentError(f"{manifest}: missing string field {key}")
    return value.strip()


def _int(raw: dict[str, Any], key: str, manifest: Path) -> int:
    value = raw.get(key)
    if not isinstance(value, int):
        raise ModuleContentError(f"{manifest}: missing integer field {key}")
    return value


def _str_list(raw: dict[str, Any], key: str, manifest: Path) -> list[str]:
    value = raw.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ModuleContentError(f"{manifest}: missing string-list field {key}")
    return [item.strip() for item in value]


def _optional_str_list(raw: dict[str, Any], key: str, manifest: Path) -> list[str]:
    value = raw.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ModuleContentError(f"{manifest}: invalid string-list field {key}")
    return [item.strip() for item in value]
