"""Regression tests for BIOL-1 LectureCreate completeness and portability."""

import json
from pathlib import Path

from src.lecture_create.main import (
    _relativize_render_metadata,
    build_module_lecture_yaml,
    term_pages,
)
from src.lecture_create.validation import validate_rendered_lecture
from src.module_content.main import load_module_content

REPO_ROOT = Path(__file__).resolve().parents[2]
COURSE_ROOT = REPO_ROOT / "course_development" / "biol-1" / "course"


def test_all_course_lecture_manifests_include_complete_authored_content(tmp_path):
    modules = sorted(COURSE_ROOT.glob("module-*/module.toml"))

    assert len(modules) == 16
    for manifest in modules:
        module = load_module_content(manifest.parent)
        rendered = build_module_lecture_yaml(module.module_dir, tmp_path / module.slug)
        for objective in module.learning_objectives:
            assert objective in rendered
        for topic in module.topics:
            assert topic in rendered
        for term in module.terms:
            assert f"{term.name}: {term.definition}" in rendered
        assert "can grow into a theory" not in rendered.lower()


def test_term_pages_are_three_items_and_preserve_order():
    module = load_module_content(COURSE_ROOT / "module-02-basic-chemistry")

    pages = term_pages(module)

    assert [len(page) for page in pages] == [3, 3, 2]
    assert [term.name for page in pages for term in page] == [term.name for term in module.terms]


def test_lecture_manifest_has_application_and_study_beats(tmp_path):
    module = load_module_content(COURSE_ROOT / "module-01-study-of-life")
    rendered = build_module_lecture_yaml(module.module_dir, tmp_path / module.slug)

    assert 'id: "module-01-study-of-life_application"' in rendered
    assert 'id: "module-01-study-of-life_study_move"' in rendered
    assert module.contents[0] in rendered
    assert module.learning_questions[-1] in rendered


def test_generated_image_paths_are_relative_to_render_workspace():
    module = load_module_content(COURSE_ROOT / "module-01-study-of-life")

    rendered = build_module_lecture_yaml(module.module_dir, Path("/tmp") / module.slug)

    assert 'image_path: "png/module-01-concept-map.png"' in rendered
    assert 'image_path: "png/module-01-process-model.png"' in rendered
    assert 'image_path: "png/module-01-retrieval-card.png"' in rendered
    assert "/Users/" not in rendered


def test_rendered_lecture_validator_rejects_incomplete_artifact(tmp_path):
    module = load_module_content(COURSE_ROOT / "module-01-study-of-life")
    lecture_dir = tmp_path / module.slug / "lectures"
    lecture_dir.mkdir(parents=True)
    (lecture_dir / "lecture.json").write_text(
        json.dumps(
            {
                "title": f"BIOL-1 Module {module.number:02d}: {module.title}",
                "sections": [{"objectives": [], "beats": []}],
            }
        ),
        encoding="utf-8",
    )

    issues = validate_rendered_lecture(module, tmp_path)

    assert any("objectives" in issue for issue in issues)
    assert any("beat sequence" in issue for issue in issues)
    assert any("narration omits" in issue for issue in issues)


def test_rendered_lecture_validator_rejects_short_measured_timeline(tmp_path):
    module = load_module_content(COURSE_ROOT / "module-01-study-of-life")
    source = (
        REPO_ROOT / "output" / "lectures" / module.slug / module.slug / "lectures" / "lecture.json"
    )
    if source.is_file():
        payload = json.loads(source.read_text(encoding="utf-8"))
    else:
        payload = {
            "title": f"BIOL-1 Module {module.number:02d}: {module.title}",
            "sections": [
                {
                    "objectives": list(module.learning_objectives),
                    "beats": [
                        {
                            "id": f"{module.slug}_duration_fixture_{index}",
                            "narration": "duration fixture",
                            "visual": {},
                            "duration_ms": 1000,
                        }
                        for index in range(14)
                    ],
                }
            ],
        }
    for beat in payload["sections"][0]["beats"]:
        beat["duration_ms"] = 1000
    lecture_dir = tmp_path / module.slug / "lectures"
    lecture_dir.mkdir(parents=True)
    (lecture_dir / "lecture.json").write_text(json.dumps(payload), encoding="utf-8")

    issues = validate_rendered_lecture(module, tmp_path / module.slug)

    assert any("measured lecture duration" in issue for issue in issues)


def test_canonical_render_config_pins_readable_video_contract():
    config = REPO_ROOT / "software" / "src" / "lecture_create" / "biol-1.yaml"
    text = config.read_text(encoding="utf-8")

    assert "width: 1920" in text
    assert "height: 1080" in text
    assert 'font: "DejaVu Sans"' in text
    assert 'layout: "standard"' in text


def test_render_metadata_rewrites_workspace_absolute_paths(tmp_path):
    output_dir = tmp_path / "module-01-test"
    lecture_dir = output_dir / output_dir.name / "lectures"
    manifest_dir = output_dir / output_dir.name / "manifests"
    lecture_dir.mkdir(parents=True)
    manifest_dir.mkdir(parents=True)
    payload = {
        "audio_path": str(output_dir / "audio" / "beat.wav"),
        "nested": {"path": str(output_dir / "png" / "map.png")},
    }
    (lecture_dir / "lecture.json").write_text(json.dumps(payload), encoding="utf-8")
    (manifest_dir / "render_manifest.json").write_text(json.dumps(payload), encoding="utf-8")

    _relativize_render_metadata(output_dir)

    normalized = json.loads((lecture_dir / "lecture.json").read_text(encoding="utf-8"))
    assert normalized == {"audio_path": "audio/beat.wav", "nested": {"path": "png/map.png"}}
