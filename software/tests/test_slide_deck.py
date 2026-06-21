from __future__ import annotations

from pathlib import Path

from src.slide_deck.main import (
    SLIDE_COUNT,
    SlideDeck,
    build_slide_deck,
    render_deck_html,
    render_module_slide_deck,
    validate_slide_deck,
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1].parent


def module_one() -> Path:
    return repo_root() / "course_development/biol-1/course/module-01-study-of-life"


def test_build_slide_deck_uses_module_manifest() -> None:
    deck = build_slide_deck(module_one())

    assert deck.module.number == 1
    assert len(deck.slides) == SLIDE_COUNT == 11
    assert validate_slide_deck(deck) == []
    assert {slide.role for slide in deck.slides} >= {
        "title-map",
        "objectives",
        "concept-map",
        "process-model",
        "retrieval",
        "lab",
    }
    assert all(slide.visual_kind for slide in deck.slides)
    svg_slides = [slide for slide in deck.slides if slide.svg]
    assert len(svg_slides) == 3
    assert {slide.role for slide in svg_slides} == {"concept-map", "process-model", "retrieval"}
    assert {slide.svg.kind for slide in svg_slides if slide.svg} == {
        "concept-map",
        "process-model",
        "retrieval-card",
    }
    for slide in svg_slides:
        assert slide.svg is not None
        assert slide.title == slide.svg.title
        assert any(deck.module.title in item for item in slide.body)
        assert any(deck.module.lab in item for item in slide.body)
        assert 3 <= len(slide.body) <= 5


def test_render_deck_html_embeds_required_visuals_and_notes() -> None:
    deck = build_slide_deck(module_one())
    full_html = render_deck_html(deck, "full")
    notes_html = render_deck_html(deck, "notes")

    assert full_html == render_deck_html(deck, "full")
    assert "Module 01" in full_html
    assert "Learning objectives" in full_html
    assert "Lab file:" in full_html
    assert "data-visual-kind=\"embedded-svg\"" in full_html
    assert "module-01-concept-map" in full_html
    assert "module-01-process-model" in full_html
    assert "module-01-retrieval-card" in full_html
    assert "module-01-concept-map.svg" in full_html
    assert "module-01-process-model.svg" in full_html
    assert "module-01-retrieval-card.svg" in full_html
    assert full_html.count("data-visual-kind=\"embedded-svg\"") == 3
    assert "Correct:" not in full_html
    assert "Teaching note:" in notes_html
    assert "Answer key:" in notes_html
    assert notes_html.count('<section class="slide') == len(deck.slides)


def test_validate_slide_deck_rejects_missing_or_duplicated_visual_spine() -> None:
    deck = build_slide_deck(module_one())
    missing = SlideDeck(deck.module, tuple(slide for slide in deck.slides if slide.role != "retrieval"))
    duplicate = SlideDeck(
        deck.module,
        tuple(
            slide if slide.role != "retrieval" else type(slide)(
                slide.title,
                slide.role,
                slide.visual_kind,
                slide.body,
                slide.note,
                next(item.svg for item in deck.slides if item.role == "concept-map"),
            )
            for slide in deck.slides
        ),
    )

    assert any("missing generated SVG slides" in issue for issue in validate_slide_deck(missing))
    assert any("must embed retrieval-card" in issue for issue in validate_slide_deck(duplicate))


def test_render_module_slide_deck_dry_run_outputs_contract_paths(tmp_path: Path) -> None:
    result = render_module_slide_deck(module_one(), tmp_path, dry_run=True)
    outputs = [Path(path).name for path in result["outputs"]]

    assert result["written"] == 0
    assert outputs == [
        "module-1-slides-full.html",
        "module-1-slides-notes.html",
        "module-1-slides-full.pdf",
        "module-1-slides-notes.pdf",
    ]
