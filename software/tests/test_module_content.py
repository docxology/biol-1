"""Tests for typed BIOL-1 module content manifests and renderers."""

from pathlib import Path

import pytest

from src.module_content.main import (
    ModuleContentError,
    load_module_content,
    render_module_materials,
)


MODULE_TOML = '''[module]
number = 1
slug = "module-01-test"
title = "Test Module"
lab = "lab-01_test.md"
topics = ["Topic A", "Topic B"]
contents = ["Use evidence", "Practice vocabulary", "Apply the lab", "Revise claims"]
learning_objectives = ["Define one idea.", "Apply one idea.", "Compare two ideas."]
study_tips = ["Review terms.", "Answer questions."]
learning_questions = ["Question 1?", "Question 2?", "Question 3?", "Question 4?", "Question 5?", "Question 6?", "Question 7?", "Question 8?"]

[[terms]]
name = "Alpha"
definition = "First term."

[[terms]]
name = "Beta"
definition = "Second term."

[[terms]]
name = "Gamma"
definition = "Third term."

[[practice_quiz]]
question = "Question A?"
options = ["Correct", "Wrong 1", "Wrong 2", "Wrong 3"]
answer = "A"
explanation = "A is correct."

[[practice_quiz]]
question = "Question B?"
options = ["Wrong 1", "Correct", "Wrong 2", "Wrong 3"]
answer = "B"
explanation = "B is correct."

[[practice_quiz]]
question = "Question C?"
options = ["Wrong 1", "Wrong 2", "Correct", "Wrong 3"]
answer = "C"
explanation = "C is correct."

[[practice_quiz]]
question = "Question D?"
options = ["Wrong 1", "Wrong 2", "Wrong 3", "Correct"]
answer = "D"
explanation = "D is correct."

[[generated_images]]
id = "concept-map"
title = "Concept Map"
kind = "concept-map"
output = "resources/generated/module-01-concept-map.svg"
prompt = "Deterministic local SVG."
central_claim = "Topic A connects vocabulary to lab evidence."
clusters = ["Course idea", "Vocabulary", "Practice"]

[[generated_images.nodes]]
id = "topic"
label = "Topic A"
detail = "Main module focus."
cluster = "Course idea"

[[generated_images.nodes]]
id = "term1"
label = "Alpha"
detail = "First term."
cluster = "Vocabulary"

[[generated_images.nodes]]
id = "term2"
label = "Beta"
detail = "Second term."
cluster = "Vocabulary"

[[generated_images.nodes]]
id = "evidence"
label = "Evidence"
detail = "Use observations."
cluster = "Practice"

[[generated_images.nodes]]
id = "lab"
label = "Lab"
detail = "Apply claims."
cluster = "Practice"

[[generated_images.edges]]
source = "topic"
target = "term1"
label = "defines"

[[generated_images.edges]]
source = "term1"
target = "evidence"
label = "supports"

[[generated_images.edges]]
source = "evidence"
target = "lab"
label = "tests"

[[generated_images.edges]]
source = "lab"
target = "term2"
label = "reveals"

[[generated_images.edges]]
source = "term2"
target = "topic"
label = "connects"

[[generated_images]]
id = "process-model"
title = "Process Model"
kind = "process-model"
output = "resources/generated/module-01-process-model.svg"
prompt = "Deterministic local SVG."
inputs = ["Topic A", "Topic B"]
outputs = ["Define one idea.", "Apply one idea."]
feedbacks = ["Lab evidence revises the claim."]
constraints = ["Practice vocabulary"]

[[generated_images.stages]]
label = "Notice"
detail = "Use evidence."

[[generated_images.stages]]
label = "Name"
detail = "Practice vocabulary."

[[generated_images.stages]]
label = "Apply"
detail = "Apply the lab."

[[generated_images.stages]]
label = "Revise"
detail = "Revise claims."

[[generated_images]]
id = "retrieval-card"
title = "Retrieval Card"
kind = "retrieval-card"
output = "resources/generated/module-01-retrieval-card.svg"
prompt = "Deterministic local SVG."
terms = ["Alpha", "Beta", "Gamma"]
lab_connection = "Lab 01 checks the module idea with evidence."

[[generated_images.prompts]]
prompt = "Question 1?"
check = "Use Alpha in the answer."

[[generated_images.prompts]]
prompt = "Question 2?"
check = "Use Beta in the answer."

[[generated_images.prompts]]
prompt = "Question 3?"
check = "Use Gamma in the answer."

[[generated_images.prompts]]
prompt = "Question 4?"
check = "Connect the claim to lab evidence."
'''


def make_module(temp_dir: Path) -> Path:
    module_dir = temp_dir / "module-01-test"
    module_dir.mkdir()
    (module_dir / "module.toml").write_text(MODULE_TOML, encoding="utf-8")
    return module_dir


def test_load_module_content_success(temp_dir):
    module_dir = make_module(temp_dir)

    module = load_module_content(module_dir)

    assert module.number == 1
    assert module.title == "Test Module"
    assert module.practice_quiz[3].answer == "D"
    assert module.generated_images[0].concept_map is not None
    assert module.generated_images[1].process_model is not None
    assert module.generated_images[2].retrieval_card is not None


def test_render_module_materials_outputs_markdown_and_svg(temp_dir):
    module_dir = make_module(temp_dir)

    result = render_module_materials(module_dir)

    assert result["written"] == 11
    assert (module_dir / "keys-to-success.md").read_text(encoding="utf-8").startswith(
        "<!-- Generated from module.toml"
    )
    assert "## Learning Objectives" in (module_dir / "keys-to-success.md").read_text(
        encoding="utf-8"
    )
    assert "# Module 1: Test Module - Practice Quiz" in (module_dir / "practice-quiz.md").read_text(
        encoding="utf-8"
    )
    assert (module_dir / "resources" / "generated" / "module-01-concept-map.svg").exists()
    assert (module_dir / "resources" / "generated" / "module-01-process-model.svg").exists()
    assert (module_dir / "resources" / "generated" / "module-01-retrieval-card.svg").exists()
    svg = (module_dir / "resources" / "generated" / "module-01-concept-map.svg").read_text(
        encoding="utf-8"
    )
    assert "role=\"img\"" in svg
    assert "palette-high-design" in svg
    assert "Topic A connects vocabulary" in svg
    assert "Linked lab: lab-01_test.md" in svg


def test_missing_manifest_fails_fast(temp_dir):
    module_dir = temp_dir / "module-01-test"
    module_dir.mkdir()

    with pytest.raises(ModuleContentError, match="Missing module manifest"):
        load_module_content(module_dir)


def test_malformed_manifest_fails_fast(temp_dir):
    module_dir = temp_dir / "module-01-test"
    module_dir.mkdir()
    (module_dir / "module.toml").write_text("[module\n", encoding="utf-8")

    with pytest.raises(ModuleContentError, match="Malformed module.toml"):
        load_module_content(module_dir)


def test_unbalanced_quiz_answers_fail(temp_dir):
    module_dir = make_module(temp_dir)
    text = (module_dir / "module.toml").read_text(encoding="utf-8")
    text = text.replace('answer = "D"', 'answer = "A"')
    (module_dir / "module.toml").write_text(text, encoding="utf-8")

    with pytest.raises(ModuleContentError, match="balance A-D"):
        load_module_content(module_dir)


def test_generated_image_must_stay_inside_module(temp_dir):
    module_dir = make_module(temp_dir)
    text = (module_dir / "module.toml").read_text(encoding="utf-8")
    text = text.replace(
        'output = "resources/generated/module-01-concept-map.svg"',
        'output = "../escape.svg"',
    )
    (module_dir / "module.toml").write_text(text, encoding="utf-8")

    with pytest.raises(ModuleContentError, match="escapes module directory"):
        load_module_content(module_dir)


def test_unknown_generated_image_kind_fails(temp_dir):
    module_dir = make_module(temp_dir)
    text = (module_dir / "module.toml").read_text(encoding="utf-8")
    text = text.replace('kind = "process-model"', 'kind = "unknown-kind"', 1)
    (module_dir / "module.toml").write_text(text, encoding="utf-8")

    with pytest.raises(ModuleContentError, match="unsupported"):
        load_module_content(module_dir)


def test_missing_explicit_visual_payload_fails(temp_dir):
    module_dir = make_module(temp_dir)
    text = (module_dir / "module.toml").read_text(encoding="utf-8")
    text = text.replace('central_claim = "Topic A connects vocabulary to lab evidence."\n', "")
    (module_dir / "module.toml").write_text(text, encoding="utf-8")

    with pytest.raises(ModuleContentError, match="central_claim"):
        load_module_content(module_dir)


def test_dangling_concept_map_edge_fails(temp_dir):
    module_dir = make_module(temp_dir)
    text = (module_dir / "module.toml").read_text(encoding="utf-8")
    text = text.replace('target = "term1"', 'target = "missing"', 1)
    (module_dir / "module.toml").write_text(text, encoding="utf-8")

    with pytest.raises(ModuleContentError, match="dangling edge"):
        load_module_content(module_dir)


def test_duplicate_generated_image_output_fails(temp_dir):
    module_dir = make_module(temp_dir)
    text = (module_dir / "module.toml").read_text(encoding="utf-8")
    text = text.replace(
        'output = "resources/generated/module-01-process-model.svg"',
        'output = "resources/generated/module-01-concept-map.svg"',
    )
    (module_dir / "module.toml").write_text(text, encoding="utf-8")

    with pytest.raises(ModuleContentError, match="outputs must be unique"):
        load_module_content(module_dir)


def test_non_svg_generated_image_output_fails(temp_dir):
    module_dir = make_module(temp_dir)
    text = (module_dir / "module.toml").read_text(encoding="utf-8")
    text = text.replace(
        'output = "resources/generated/module-01-retrieval-card.svg"',
        'output = "resources/generated/module-01-retrieval-card.png"',
    )
    (module_dir / "module.toml").write_text(text, encoding="utf-8")

    with pytest.raises(ModuleContentError, match="expected resources/generated/module-01-retrieval-card.svg"):
        load_module_content(module_dir)
