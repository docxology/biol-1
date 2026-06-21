"""Generated BIOL-1 slide decks from structured module manifests."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from src.module_content.main import GeneratedImage, ModuleContent, load_module_content

DeckVariant = Literal["full", "notes"]
SLIDE_COUNT = 11


class SlideDeckError(ValueError):
    """Raised when generated slide decks are malformed."""


@dataclass(frozen=True)
class Slide:
    title: str
    role: str
    visual_kind: str
    body: tuple[str, ...]
    note: str
    svg: GeneratedImage | None = None


@dataclass(frozen=True)
class SlideDeck:
    module: ModuleContent
    slides: tuple[Slide, ...]


def build_slide_deck(module_dir: Path | str) -> SlideDeck:
    """Build an in-memory slide deck from a module manifest."""
    module = load_module_content(module_dir)
    visuals = {image.id: image for image in module.generated_images}
    required = {"concept-map", "process-model", "retrieval-card"}
    missing = sorted(required - visuals.keys())
    if missing:
        raise SlideDeckError(f"{module.slug} missing generated visuals: {', '.join(missing)}")

    slides = (
        Slide(
            "Module map",
            "title-map",
            "module-map",
            (
                f"Module {module.number:02d}: {module.title}",
                f"Connected lab: {module.lab}",
                "Use this deck as the visual path through the module's evidence and retrieval work.",
            ),
            "Open by naming the module claim and pointing students to the lab as the evidence surface.",
        ),
        Slide(
            "Learning objectives",
            "objectives",
            "objective-ladder",
            module.learning_objectives[:5],
            "Frame objectives as actions students should be able to perform, not facts to copy.",
        ),
        Slide(
            "Topic sequence",
            "topics",
            "topic-sequence",
            tuple(f"{topic}: {content}" for topic, content in zip(module.topics, module.contents, strict=True)),
            "Show the module as an ordered explanation so students can locate each new idea.",
        ),
        Slide(
            visuals["concept-map"].title,
            "concept-map",
            "embedded-svg",
            _concept_map_bullets(module, visuals["concept-map"]),
            "Ask students to explain one edge in their own words before moving on.",
            visuals["concept-map"],
        ),
        Slide(
            visuals["process-model"].title,
            "process-model",
            "embedded-svg",
            _process_model_bullets(module, visuals["process-model"]),
            "Emphasize where the process can fail, slow down, or be revised by evidence.",
            visuals["process-model"],
        ),
        Slide(
            "Terms as evidence handles",
            "terms",
            "term-grid",
            tuple(f"{term.name}: {term.definition}" for term in module.terms[:6]),
            "Treat terms as handles for reasoning. Each term should help explain a claim or observation.",
        ),
        Slide(
            "Lab connection",
            "lab",
            "lab-flow",
            (
                f"Lab file: {module.lab}",
                f"Lab evidence should test or illustrate: {module.topics[min(2, len(module.topics) - 1)]}",
                "Students should leave with a concrete observation, comparison, or model tied to the module claim.",
            ),
            "Make the lab connection explicit before students encounter the activity.",
        ),
        Slide(
            "Contrast check",
            "contrast",
            "contrast-panel",
            (
                f"Do not stop at: {module.contents[0]}",
                f"Stronger explanation: {module.contents[-1]}",
                "The goal is to move from a named idea to a testable biological explanation.",
            ),
            "Use this slide to prevent shallow vocabulary-only learning.",
        ),
        Slide(
            visuals["retrieval-card"].title,
            "retrieval",
            "embedded-svg",
            _retrieval_card_bullets(module, visuals["retrieval-card"]),
            "Pause here. Students answer first without notes, then compare to the checks.",
            visuals["retrieval-card"],
        ),
        Slide(
            "Practice quiz bridge",
            "quiz",
            "quiz-bridge",
            tuple(f"{idx}. {quiz.question}" for idx, quiz in enumerate(module.practice_quiz[:4], 1)),
            "Use the quiz as formative feedback. Answer key: "
            + ", ".join(f"{idx}={quiz.answer}" for idx, quiz in enumerate(module.practice_quiz[:4], 1)),
        ),
        Slide(
            "Synthesis and exit ticket",
            "synthesis",
            "exit-ticket",
            (
                f"Exit claim: explain {module.topics[0].lower()} using evidence from {module.lab}.",
                f"Must include: {', '.join(term.name for term in module.terms[:3])}.",
                "Revision prompt: what evidence would change your explanation?",
            ),
            "End with a claim-evidence-reasoning exit ticket connected to the same module data.",
        ),
    )
    deck = SlideDeck(module=module, slides=slides)
    issues = validate_slide_deck(deck)
    if issues:
        raise SlideDeckError("; ".join(issues))
    return deck


def validate_slide_deck(deck: SlideDeck) -> list[str]:
    """Return validation issues for a generated deck."""
    issues: list[str] = []
    if len(deck.slides) != SLIDE_COUNT:
        issues.append(f"{deck.module.slug} has {len(deck.slides)} slides; expected {SLIDE_COUNT}")
    roles = [slide.role for slide in deck.slides]
    if len(set(roles)) != len(roles):
        issues.append(f"{deck.module.slug} has duplicate slide roles")
    required_roles = {
        "title-map",
        "objectives",
        "topics",
        "concept-map",
        "process-model",
        "terms",
        "lab",
        "contrast",
        "retrieval",
        "quiz",
        "synthesis",
    }
    missing_roles = sorted(required_roles - set(roles))
    if missing_roles:
        issues.append(f"{deck.module.slug} missing slide roles: {', '.join(missing_roles)}")
    expected_svg_roles = {
        "concept-map": "concept-map",
        "process-model": "process-model",
        "retrieval": "retrieval-card",
    }
    svg_roles: dict[str, str] = {}
    for slide in deck.slides:
        if not slide.title.strip():
            issues.append(f"{deck.module.slug} has an untitled slide")
        if not slide.visual_kind.strip():
            issues.append(f"{deck.module.slug} slide {slide.role} lacks a visual kind")
        if not slide.body:
            issues.append(f"{deck.module.slug} slide {slide.role} has no body content")
        if not slide.svg and slide.visual_kind == "embedded-svg":
            issues.append(f"{deck.module.slug} slide {slide.role} embeds no generated SVG")
        if slide.svg:
            if slide.visual_kind != "embedded-svg":
                issues.append(f"{deck.module.slug} slide {slide.role} has SVG without embedded-svg visual kind")
            if slide.svg.kind not in {"concept-map", "process-model", "retrieval-card"}:
                issues.append(f"{deck.module.slug} slide {slide.role} has unsupported SVG kind {slide.svg.kind}")
            if slide.role not in expected_svg_roles:
                issues.append(f"{deck.module.slug} slide {slide.role} has unexpected generated SVG")
            elif expected_svg_roles[slide.role] != slide.svg.kind:
                issues.append(
                    f"{deck.module.slug} slide {slide.role} must embed "
                    f"{expected_svg_roles[slide.role]}, found {slide.svg.kind}"
                )
            svg_roles[slide.role] = slide.svg.kind
            if not any(deck.module.lab in item for item in slide.body):
                issues.append(f"{deck.module.slug} slide {slide.role} does not reference linked lab")
            if not any(deck.module.title in item for item in slide.body):
                issues.append(f"{deck.module.slug} slide {slide.role} does not reference module title")
    missing_svg_roles = sorted(set(expected_svg_roles) - set(svg_roles))
    if missing_svg_roles:
        issues.append(f"{deck.module.slug} missing generated SVG slides: {', '.join(missing_svg_roles)}")
    if len(set(svg_roles.values())) != len(svg_roles):
        issues.append(f"{deck.module.slug} reuses a generated SVG across multiple slides")
    return issues


def _concept_map_bullets(module: ModuleContent, image: GeneratedImage) -> tuple[str, ...]:
    spec = image.concept_map
    if spec is None:
        return (f"Module focus: {module.title}", f"Lab connection: {module.lab}")
    nodes = ", ".join(node.label for node in spec.nodes[:3])
    edge = spec.edges[0].label if spec.edges else "connections explain evidence"
    return (
        f"Module focus: {module.title}",
        f"Central claim: {spec.central_claim}",
        f"Key nodes to connect: {nodes}",
        f"Reasoning move: use '{edge}' to explain relationships, not memorize terms.",
        f"Lab connection: {module.lab} supplies an evidence surface for the map.",
    )


def _process_model_bullets(module: ModuleContent, image: GeneratedImage) -> tuple[str, ...]:
    spec = image.process_model
    if spec is None:
        return (f"Module focus: {module.title}", f"Lab connection: {module.lab}")
    stage_labels = " -> ".join(stage.label for stage in spec.stages[:4])
    inputs = ", ".join(spec.inputs[:2])
    outputs = ", ".join(spec.outputs[:2])
    feedback = spec.feedbacks[0] if spec.feedbacks else "feedback changes the next step"
    return (
        f"Module focus: {module.title}",
        f"Trace the model: {stage_labels}",
        f"Inputs become outputs: {inputs} -> {outputs}",
        f"Feedback check: {feedback}",
        f"Lab connection: {module.lab} gives students a process to observe or test.",
    )


def _retrieval_card_bullets(module: ModuleContent, image: GeneratedImage) -> tuple[str, ...]:
    spec = image.retrieval_card
    if spec is None:
        return (f"Module focus: {module.title}", f"Lab connection: {module.lab}")
    prompt = spec.prompts[0].prompt if spec.prompts else module.learning_questions[0]
    check = spec.prompts[0].check if spec.prompts else "answer with evidence"
    terms = ", ".join(spec.terms[:3])
    return (
        f"Module focus: {module.title}",
        f"Retrieval prompt: {prompt}",
        f"Answer check: {check}",
        f"Required terms: {terms}",
        f"Lab connection: {module.lab}; {spec.lab_connection}",
    )


def render_module_slide_deck(
    module_dir: Path | str,
    slides_root: Path | str,
    dry_run: bool = False,
) -> dict[str, object]:
    """Render full and notes decks for one module."""
    deck = build_slide_deck(module_dir)
    root = Path(slides_root)
    generated_root = root / "generated"
    outputs = [
        generated_root / f"module-{deck.module.number}-slides-full.html",
        generated_root / f"module-{deck.module.number}-slides-notes.html",
        root / f"module-{deck.module.number}-slides-full.pdf",
        root / f"module-{deck.module.number}-slides-notes.pdf",
    ]
    if dry_run:
        return {"module": deck.module.slug, "outputs": [str(path) for path in outputs], "written": 0}

    generated_root.mkdir(parents=True, exist_ok=True)
    full_html = render_deck_html(deck, "full")
    notes_html = render_deck_html(deck, "notes")
    outputs[0].write_text(full_html, encoding="utf-8")
    outputs[1].write_text(notes_html, encoding="utf-8")
    from weasyprint import HTML

    HTML(string=full_html, base_url=str(deck.module.module_dir)).write_pdf(outputs[2])
    HTML(string=notes_html, base_url=str(deck.module.module_dir)).write_pdf(outputs[3])
    return {"module": deck.module.slug, "outputs": [str(path) for path in outputs], "written": len(outputs)}


def render_course_slide_decks(
    course_root: Path | str,
    module_filter: int | None = None,
    dry_run: bool = False,
) -> dict[str, object]:
    """Render generated slide decks for every module in a course."""
    course_path = Path(course_root)
    slides_root = course_path / "resources" / "slides"
    modules = _module_dirs(course_path, module_filter)
    results = [render_module_slide_deck(module_dir, slides_root, dry_run=dry_run) for module_dir in modules]
    written = sum(value for result in results for value in [result.get("written")] if isinstance(value, int))
    return {"course": str(course_path), "module_count": len(results), "modules": results, "written": written}


def describe_course_slide_decks(course_root: Path | str, module_filter: int | None = None) -> str:
    """Return a dry-run report for generated slide decks."""
    lines = ["Generated slide decks:"]
    for module_dir in _module_dirs(Path(course_root), module_filter):
        deck = build_slide_deck(module_dir)
        lines.append(f"  {deck.module.slug}: {len(deck.slides)} slides, full + notes PDFs")
    return "\n".join(lines)


def render_deck_html(deck: SlideDeck, variant: DeckVariant) -> str:
    """Render a full or notes deck as print-ready HTML."""
    notes_mode = variant == "notes"
    title = f"Module {deck.module.number:02d}: {deck.module.title} Slides ({variant})"
    parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        f"<title>{_e(title)}</title>",
        "<style>",
        _deck_css(notes_mode),
        "</style>",
        "</head>",
        "<body>",
    ]
    for index, slide in enumerate(deck.slides, 1):
        parts.append(_render_slide(deck, slide, index, notes_mode))
    parts.extend(["</body>", "</html>"])
    return "\n".join(parts)


def _render_slide(deck: SlideDeck, slide: Slide, index: int, notes_mode: bool) -> str:
    visual = _render_visual(deck, slide)
    body_items = "".join(f"<li>{_e(item)}</li>" for item in slide.body[:6])
    note_html = f'<aside class="speaker-note"><strong>Teaching note:</strong> {_e(slide.note)}</aside>' if notes_mode else ""
    return f"""
<section class="slide slide-{_slug(slide.role)}" data-slide-role="{_e(slide.role)}" data-visual-kind="{_e(slide.visual_kind)}">
  <div class="slide-ribbon">BIOL-1 · Module {deck.module.number:02d} · Slide {index:02d}</div>
  <div class="slide-grid">
    <div class="slide-copy">
      <p class="eyebrow">{_e(deck.module.title)}</p>
      <h1>{_e(slide.title)}</h1>
      <ul>{body_items}</ul>
    </div>
    <div class="visual-frame" data-visual="{_e(slide.visual_kind)}">{visual}</div>
  </div>
  {note_html}
</section>
""".strip()


def _render_visual(deck: SlideDeck, slide: Slide) -> str:
    module = deck.module
    if slide.svg:
        svg_path = module.module_dir / slide.svg.output
        svg_text = svg_path.read_text(encoding="utf-8") if svg_path.exists() else ""
        svg_text = _scoped_svg_ids(svg_text, f"m{module.number}-{_slug(slide.role)}")
        source = Path(slide.svg.output).name
        return f'<div class="embedded-svg" data-source="{_e(source)}">{svg_text}</div>'
    if slide.visual_kind == "module-map":
        chips = "".join(f"<span>{_e(topic)}</span>" for topic in module.topics)
        return f'<div class="module-orbit"><strong>Module {module.number:02d}</strong>{chips}<em>{_e(module.lab)}</em></div>'
    if slide.visual_kind == "objective-ladder":
        return _ordered_cards("Objective", module.learning_objectives[:5])
    if slide.visual_kind == "topic-sequence":
        return _ordered_cards("Topic", module.topics)
    if slide.visual_kind == "term-grid":
        cards = "".join(f"<div><b>{_e(term.name)}</b><span>{_e(term.definition)}</span></div>" for term in module.terms[:6])
        return f'<div class="term-grid">{cards}</div>'
    if slide.visual_kind == "lab-flow":
        return _flow_diagram(("Question", "Evidence", "Claim"), (module.topics[0], module.lab, module.learning_objectives[0]))
    if slide.visual_kind == "contrast-panel":
        return f'<div class="contrast"><div><b>Surface</b><span>{_e(module.contents[0])}</span></div><div><b>Deeper</b><span>{_e(module.contents[-1])}</span></div></div>'
    if slide.visual_kind == "quiz-bridge":
        return _ordered_cards("Quiz", tuple(quiz.answer for quiz in module.practice_quiz[:4]))
    if slide.visual_kind == "exit-ticket":
        return _flow_diagram(("Claim", "Evidence", "Revision"), (module.topics[0], module.lab, "What would change your mind?"))
    return '<div class="visual-placeholder">Visual surface</div>'


def _ordered_cards(label: str, values: tuple[str, ...]) -> str:
    cards = "".join(
        f'<div class="step-card"><b>{label} {idx}</b><span>{_e(value)}</span></div>'
        for idx, value in enumerate(values, 1)
    )
    return f'<div class="ordered-cards">{cards}</div>'


def _flow_diagram(labels: tuple[str, str, str], values: tuple[str, str, str]) -> str:
    cells = "".join(
        f'<div class="flow-cell"><b>{_e(label)}</b><span>{_e(value)}</span></div>'
        for label, value in zip(labels, values, strict=True)
    )
    return f'<div class="flow-diagram">{cells}</div>'


def _deck_css(notes_mode: bool) -> str:
    note_css = "" if notes_mode else ".speaker-note{display:none}"
    return f"""
@page {{ size: 16in 9in; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #f4efe4; color: #17211c; font-family: Avenir Next, Trebuchet MS, sans-serif; }}
.slide {{ page-break-after: always; width: 16in; height: 9in; padding: .44in; position: relative; overflow: hidden; background: radial-gradient(circle at 12% 18%, #fff7d6 0, transparent 28%), linear-gradient(135deg, #f7efe1 0%, #d7e6dc 100%); }}
.slide::after {{ content: ""; position: absolute; right: -.5in; bottom: -.55in; width: 5.4in; height: 5.4in; border-radius: 50%; background: rgba(25, 92, 75, .12); }}
.slide-ribbon {{ position: absolute; top: .2in; right: .35in; font-size: 11pt; letter-spacing: .08em; text-transform: uppercase; color: #41564f; }}
.slide-grid {{ display: grid; grid-template-columns: 5.05in 1fr; gap: .36in; height: 100%; align-items: stretch; }}
.slide-copy {{ border-left: .08in solid #bb5a3a; padding: .38in .18in .2in .28in; z-index: 1; }}
.eyebrow {{ margin: 0 0 .18in; font-size: 13pt; text-transform: uppercase; letter-spacing: .11em; color: #79513c; }}
h1 {{ margin: 0 0 .28in; font-family: Georgia, serif; font-size: 34pt; line-height: 1.02; color: #102820; }}
ul {{ list-style: none; padding: 0; margin: 0; display: grid; gap: .14in; }}
li {{ font-size: 15pt; line-height: 1.25; padding-left: .2in; position: relative; }}
li::before {{ content: ""; position: absolute; left: 0; top: .28em; width: .08in; height: .08in; border-radius: 50%; background: #bb5a3a; }}
.visual-frame {{ z-index: 1; min-height: 7.8in; border: 1px solid rgba(32, 55, 47, .22); border-radius: .22in; background: rgba(255,255,255,.72); padding: .22in; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
.embedded-svg svg {{ width: 100%; max-height: 7.25in; display: block; }}
.module-orbit {{ width: 100%; height: 100%; display: grid; grid-template-columns: repeat(2, 1fr); gap: .18in; align-content: center; }}
.module-orbit strong {{ grid-column: 1 / -1; font: 700 34pt Georgia, serif; color: #195c4b; }}
.module-orbit span, .module-orbit em, .step-card, .term-grid div, .flow-cell, .contrast div {{ background: #fff9ea; border: 1px solid rgba(187,90,58,.35); border-radius: .16in; padding: .16in; font-size: 15pt; line-height: 1.22; }}
.module-orbit em {{ grid-column: 1 / -1; color: #66422f; }}
.ordered-cards {{ display: grid; gap: .12in; width: 100%; }}
.step-card b, .term-grid b, .flow-cell b, .contrast b {{ display: block; color: #bb5a3a; margin-bottom: .04in; text-transform: uppercase; letter-spacing: .06em; font-size: 10pt; }}
.term-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: .14in; width: 100%; }}
.term-grid span, .step-card span, .flow-cell span, .contrast span {{ display: block; }}
.flow-diagram, .contrast {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: .18in; align-items: center; width: 100%; }}
.contrast {{ grid-template-columns: repeat(2, 1fr); }}
.speaker-note {{ position: absolute; left: .55in; right: .55in; bottom: .18in; z-index: 2; background: #102820; color: #fff7d6; border-radius: .12in; padding: .11in .16in; font-size: 11pt; }}
{note_css}
""".strip()


def _module_dirs(course_root: Path, module_filter: int | None) -> list[Path]:
    course_dir = course_root / "course"
    modules = sorted(path for path in course_dir.glob("module-*") if path.is_dir())
    if module_filter is not None:
        modules = [path for path in modules if re.match(rf"module-0*{module_filter}\b", path.name)]
    return modules


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _scoped_svg_ids(svg_text: str, prefix: str) -> str:
    ids = re.findall(r'id="([^"]+)"', svg_text)
    scoped = svg_text
    for value in ids:
        replacement = f"{prefix}-{value}"
        scoped = scoped.replace(f'id="{value}"', f'id="{replacement}"')
        scoped = scoped.replace(f'url(#{value})', f'url(#{replacement})')
        scoped = scoped.replace(f'href="#{value}"', f'href="#{replacement}"')
        scoped = scoped.replace(f'xlink:href="#{value}"', f'xlink:href="#{replacement}"')
    return scoped


def _e(value: object) -> str:
    return html.escape(str(value), quote=True)
