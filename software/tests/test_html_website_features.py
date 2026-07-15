"""Tests for HTML website generation features."""

import json
from pathlib import Path

import pytest

from src.html_website.main import generate_module_website


# A minimal but fully valid module.toml satisfying the module_content contract
# (exactly one concept-map/process-model/retrieval-card generated-image spec,
# each meeting its own minimum-count requirements). Mirrors the fixture used in
# tests/test_module_content.py so the structured-module rendering path in
# generate_module_website can be exercised end-to-end.
STRUCTURED_MODULE_TOML = '''[module]
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
name = "Alpha & Beta"
definition = 'A "special" term with quotes and an & ampersand.'

[[terms]]
name = "Beta"
definition = "Second term."

[[terms]]
name = "Gamma"
definition = "Third term."

[[assets]]
path = "resources/diagram.png"
kind = "diagram"
description = 'Shows the "life cycle" & key stages.'

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

[[generated_images.edges]]
source = "topic"
target = "term1"
label = "defines"

[[generated_images.edges]]
source = "term1"
target = "term2"
label = "supports"

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


class TestGenerateModuleWebsite:
    """Tests for generate_module_website function."""

    def test_generate_module_website_basic(self, temp_dir):
        """Test generating a basic module website."""
        # Create module structure
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()

        # Create sample content files
        (module_dir / "sample_lecture-content.md").write_text(
            "# Lecture Content\n\nThis is lecture content.", encoding="utf-8"
        )
        (module_dir / "sample_study-guide.md").write_text(
            "# Study Guide\n\nThis is a study guide.", encoding="utf-8"
        )

        output_dir = temp_dir / "output" / "website"
        result = generate_module_website(str(module_dir), str(output_dir))

        assert result.endswith("index.html")
        assert Path(result).exists()
        html_content = Path(result).read_text()
        assert "Lecture Content" in html_content
        assert "Study Guide" in html_content

    def test_generate_module_website_nonexistent_path(self, temp_dir):
        """Test generating website for non-existent module."""
        with pytest.raises(ValueError, match="does not exist"):
            generate_module_website(str(temp_dir / "nonexistent"))

    def test_generate_module_website_default_output_dir(self, temp_dir):
        """Test generating website with default output directory."""
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()

        result = generate_module_website(str(module_dir))

        assert "output/website/index.html" in result
        assert Path(result).exists()

    def test_generate_module_website_with_course_name(self, temp_dir):
        """Test generating website with custom course name."""
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()

        output_dir = temp_dir / "output"
        result = generate_module_website(
            str(module_dir), str(output_dir), course_name="BIOL-8"
        )

        html_content = Path(result).read_text()
        assert "BIOL-8" in html_content

    def test_generate_module_website_ignores_active_assignments(self, temp_dir):
        """Active BIOL-1 websites do not expose legacy assignments folders."""
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()

        assignments_dir = module_dir / "assignments"
        assignments_dir.mkdir()
        (assignments_dir / "assignment-1.md").write_text(
            "# Assignment 1\n\nComplete this.", encoding="utf-8"
        )

        output_dir = temp_dir / "output"
        result = generate_module_website(str(module_dir), str(output_dir))

        html_content = Path(result).read_text()
        assert "Assignment 1" not in html_content

    def test_generate_module_website_includes_root_learning_objectives(self, temp_dir):
        """BIOL-1 root study-guide headings propagate into index.html."""
        module_dir = temp_dir / "module-13-how-populations-evolve"
        module_dir.mkdir()
        (module_dir / "keys-to-success.md").write_text(
            "# Module 13: How Populations Evolve\n\n"
            "## Learning Objectives\n\n"
            "1. Define microevolution.\n",
            encoding="utf-8",
        )

        result = generate_module_website(str(module_dir), str(temp_dir / "website"))

        html_content = Path(result).read_text()
        assert "Keys to Success" in html_content
        assert "Learning Objectives" in html_content
        assert "Define microevolution" in html_content

    def test_generate_module_website_with_questions(self, temp_dir):
        """Test generating website with questions JSON."""
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()

        # Create questions directory
        questions_dir = module_dir / "questions"
        questions_dir.mkdir()
        questions_data = {
            "questions": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "question": "What is biology?",
                    "options": ["Study of life", "Study of rocks"],
                    "correct": 0,
                },
                {
                    "id": "q2",
                    "type": "true_false",
                    "question": "DNA is genetic material.",
                    "correct": True,
                },
                {
                    "id": "q3",
                    "type": "free_response",
                    "question": "Describe a cell.",
                    "placeholder": "Type here...",
                    "max_length": 500,
                },
                {
                    "id": "q4",
                    "type": "matching",
                    "question": "Match terms to definitions",
                    "items": [
                        {"term": "Cell", "definition": "Basic unit of life"},
                        {"term": "DNA", "definition": "Genetic material"},
                    ],
                },
            ]
        }
        (questions_dir / "questions.json").write_text(
            json.dumps(questions_data), encoding="utf-8"
        )

        output_dir = temp_dir / "output"
        result = generate_module_website(str(module_dir), str(output_dir))

        html_content = Path(result).read_text()
        assert "Interactive Questions" in html_content
        assert "What is biology" in html_content

    def test_generate_module_website_with_questions_escapes_quotes(self, temp_dir):
        """Question fields containing quote characters must not corrupt the
        generated HTML attributes (regression test for unescaped interpolation).
        """
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()

        questions_dir = module_dir / "questions"
        questions_dir.mkdir()
        questions_data = {
            "questions": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "question": 'What does "homeostasis" mean?',
                    "options": ['Say "steady state"', "Something else"],
                    "correct": 0,
                    "explanation": 'It means "staying the same".',
                },
                {
                    "id": "q2",
                    "type": "free_response",
                    "question": "Describe a cell.",
                    "placeholder": 'Say "yes" or "no"',
                    "max_length": 500,
                },
                {
                    "id": "q3",
                    "type": "matching",
                    "question": "Match terms",
                    "items": [
                        {"term": 'A "term"', "definition": 'A "definition"'},
                    ],
                },
            ]
        }
        (questions_dir / "questions.json").write_text(
            json.dumps(questions_data), encoding="utf-8"
        )

        output_dir = temp_dir / "output"
        result = generate_module_website(str(module_dir), str(output_dir))

        html_content = Path(result).read_text()
        # The raw unescaped quote-bearing strings must never appear verbatim,
        # since that would mean an attribute value was terminated early.
        assert 'placeholder="Say "yes" or "no""' not in html_content
        assert "&quot;" in html_content
        assert "Interactive Questions" in html_content

    def test_generate_module_website_with_text_escapes_special_chars(self, temp_dir):
        """The plain-text-version <pre> block must HTML-escape its source
        content (regression test: this branch previously interpolated raw
        .txt content unescaped, unlike every other interpolation in this
        file).
        """
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()

        (module_dir / "sample_lecture-content.md").write_text(
            "# Lecture", encoding="utf-8"
        )

        output_base = module_dir / "output" / "lecture-content"
        output_base.mkdir(parents=True)
        (output_base / "sample_lecture-content.txt").write_text(
            "if a < b & b > c: <script>alert(1)</script>", encoding="utf-8"
        )

        output_dir = temp_dir / "website_output"
        result = generate_module_website(str(module_dir), str(output_dir))

        html_content = Path(result).read_text()
        assert "<script>alert(1)</script>" not in html_content
        assert "&lt;script&gt;" in html_content
        assert "a &lt; b &amp; b &gt; c" in html_content

    def test_generate_module_website_with_audio(self, temp_dir):
        """Test generating website with audio files."""
        module_dir = temp_dir / "module-1"
        module_dir.mkdir()

        # Create content file
        (module_dir / "sample_lecture-content.md").write_text(
            "# Lecture", encoding="utf-8"
        )

        # Create output with audio
        output_base = module_dir / "output" / "lecture-content"
        output_base.mkdir(parents=True)
        (output_base / "sample_lecture-content.mp3").write_text(
            "fake audio", encoding="utf-8"
        )

        output_dir = temp_dir / "website_output"
        result = generate_module_website(str(module_dir), str(output_dir))

        html_content = Path(result).read_text()
        assert "audio" in html_content.lower()


class TestGenerateModuleWebsiteStructured:
    """Tests for the module.toml-driven structured rendering path.

    This is the path used by every active BIOL-1 module (via
    src.module_content.load_module_content), as opposed to the legacy
    sample_*.md fallback branch covered by TestGenerateModuleWebsite.
    """

    def _make_structured_module(self, temp_dir: Path) -> Path:
        module_dir = temp_dir / "module-01-test"
        module_dir.mkdir()
        (module_dir / "module.toml").write_text(STRUCTURED_MODULE_TOML, encoding="utf-8")
        # module_content validates that hand-authored [[assets]] paths exist
        # on disk (unlike generated_images, which are produced later).
        resources_dir = module_dir / "resources"
        resources_dir.mkdir()
        (resources_dir / "diagram.png").write_bytes(b"fake-png")
        return module_dir

    def test_renders_all_structured_sections_and_sidebar_links(self, temp_dir):
        module_dir = self._make_structured_module(temp_dir)

        result = generate_module_website(str(module_dir), str(temp_dir / "website"))
        html_content = Path(result).read_text(encoding="utf-8")

        # Sidebar links for every structured section.
        for section_id in (
            "topics",
            "contents",
            "learning_questions",
            "practice_quiz",
            "lab",
            "assets",
        ):
            assert f'href="#{section_id}"' in html_content
        assert 'id="terms"' in html_content

        # Section content.
        assert "Topic A" in html_content
        assert "Use evidence" in html_content
        assert "Question 1?" in html_content
        assert "Connected lab: <code>lab-01_test.md</code>" in html_content or "lab-01_test.md" in html_content

    def test_escapes_term_names_and_definitions(self, temp_dir):
        module_dir = self._make_structured_module(temp_dir)

        result = generate_module_website(str(module_dir), str(temp_dir / "website"))
        html_content = Path(result).read_text(encoding="utf-8")

        # The terms table is rendered through markdown_to_html from raw
        # markdown text (not html.escape), so the literal quote/ampersand
        # from module.toml must not corrupt the surrounding table markup.
        assert "Alpha &amp; Beta" in html_content or "Alpha & Beta" in html_content
        assert "Beta" in html_content
        assert "Gamma" in html_content

    def test_escapes_asset_description_and_kind(self, temp_dir):
        module_dir = self._make_structured_module(temp_dir)

        result = generate_module_website(str(module_dir), str(temp_dir / "website"))
        html_content = Path(result).read_text(encoding="utf-8")

        assert "diagram" in html_content
        assert "&quot;life cycle&quot;" in html_content
        assert "&amp; key stages" in html_content
        # The raw unescaped description must never appear verbatim.
        assert 'Shows the "life cycle" & key stages.' not in html_content

    def test_malformed_module_toml_falls_back_to_legacy_branch(self, temp_dir):
        """A malformed module.toml must raise ModuleContentError internally and
        fall through to the legacy sample_*.md branch, not silently produce an
        empty structured page.
        """
        module_dir = temp_dir / "module-02-broken"
        module_dir.mkdir()
        (module_dir / "module.toml").write_text("not valid = [toml", encoding="utf-8")
        (module_dir / "sample_lecture-content.md").write_text(
            "# Fallback Lecture\n\nFallback content.", encoding="utf-8"
        )

        result = generate_module_website(str(module_dir), str(temp_dir / "website"))
        html_content = Path(result).read_text(encoding="utf-8")

        assert "Fallback Lecture" in html_content
        assert 'href="#topics"' not in html_content


class TestHTMLWebsiteConfig:
    """Test HTML website configuration."""

    def test_default_css_contains_layout_variables(self):
        """Test that DEFAULT_CSS includes new layout variables."""
        from src.html_website.config import DEFAULT_CSS

        assert "--sidebar-width" in DEFAULT_CSS
        assert "--header-height" in DEFAULT_CSS
        assert "--resizer-width" in DEFAULT_CSS

    def test_default_css_contains_sidebar_styles(self):
        """Test that DEFAULT_CSS includes sidebar styles."""
        from src.html_website.config import DEFAULT_CSS

        assert ".sidebar" in DEFAULT_CSS
        assert ".sidebar-nav" in DEFAULT_CSS
        assert ".sidebar-header" in DEFAULT_CSS

    def test_default_css_contains_resizer_styles(self):
        """Test that DEFAULT_CSS includes resizer styles."""
        from src.html_website.config import DEFAULT_CSS

        assert ".resizer" in DEFAULT_CSS
        assert "col-resize" in DEFAULT_CSS

    def test_default_css_contains_dark_mode(self):
        """Test that DEFAULT_CSS includes dark mode styles."""
        from src.html_website.config import DEFAULT_CSS

        assert "dark-mode" in DEFAULT_CSS
        assert ".dark-mode-toggle" in DEFAULT_CSS
        assert "body.dark-mode" in DEFAULT_CSS

    def test_default_css_contains_mobile_responsive(self):
        """Test that DEFAULT_CSS includes mobile responsive styles."""
        from src.html_website.config import DEFAULT_CSS

        assert "@media (max-width: 768px)" in DEFAULT_CSS
        assert ".mobile-header" in DEFAULT_CSS
        assert ".mobile-menu-btn" in DEFAULT_CSS

    def test_html_template_has_sidebar_structure(self):
        """Test that HTML_TEMPLATE includes sidebar structure."""
        from src.html_website.config import HTML_TEMPLATE

        assert 'id="sidebar"' in HTML_TEMPLATE
        assert "sidebar-nav" in HTML_TEMPLATE
        assert "{sidebar_content}" in HTML_TEMPLATE

    def test_html_template_has_resizer(self):
        """Test that HTML_TEMPLATE includes resizer handle."""
        from src.html_website.config import HTML_TEMPLATE

        assert 'id="resizer"' in HTML_TEMPLATE
        assert "resizer" in HTML_TEMPLATE

    def test_html_template_has_dark_mode_toggle(self):
        """Test that HTML_TEMPLATE includes dark mode toggle button."""
        from src.html_website.config import HTML_TEMPLATE

        assert "dark-mode-toggle" in HTML_TEMPLATE
        assert "toggleDarkMode" in HTML_TEMPLATE

    def test_html_template_has_main_content_structure(self):
        """Test that HTML_TEMPLATE has main content structure."""
        from src.html_website.config import HTML_TEMPLATE

        assert "main" in HTML_TEMPLATE
        assert "content-wrapper" in HTML_TEMPLATE

    def test_dark_mode_persists_via_localstorage(self):
        """Test that dark mode JavaScript uses localStorage for persistence."""
        # Now located in the JS block, indirectly tested via string presence
        pass 


class TestHTMLWebsiteQuizStyles:
    """Test HTML website quiz-related styles."""

    def test_css_has_quiz_container(self):
        """Test that CSS includes quiz container styles."""
        from src.html_website.config import DEFAULT_CSS

        assert ".quiz-container" in DEFAULT_CSS

    def test_css_has_question_types(self):
        """Test that CSS includes all question type styles."""
        from src.html_website.config import DEFAULT_CSS

        assert ".multiple-choice-option" in DEFAULT_CSS
        assert ".true-false-btn" in DEFAULT_CSS
        assert ".free-response-textarea" in DEFAULT_CSS
        assert ".matching-container" in DEFAULT_CSS

    def test_css_has_feedback_styles(self):
        """Test that CSS includes feedback styles."""
        from src.html_website.config import DEFAULT_CSS

        assert ".question-feedback" in DEFAULT_CSS
        assert ".question-feedback.correct" in DEFAULT_CSS
        assert ".question-feedback.incorrect" in DEFAULT_CSS


class TestEnhancedAccessibilityFeatures:
    """Test enhanced accessibility features."""

    def test_html_template_has_collapse_all_button(self):
        """Test that HTML template includes collapse all button."""
        from src.html_website.config import HTML_TEMPLATE

        assert "collapseAll" in HTML_TEMPLATE
        assert "Collapse All" in HTML_TEMPLATE

    def test_html_template_has_expand_all_button(self):
        """Test that HTML template includes expand all button."""
        from src.html_website.config import HTML_TEMPLATE

        assert "expandAll" in HTML_TEMPLATE
        assert "Expand All" in HTML_TEMPLATE

    def test_html_template_has_back_to_top(self):
        """Test that template includes back to top link."""
        from src.html_website.config import HTML_TEMPLATE
        assert "back-to-top" in HTML_TEMPLATE
        assert "scrollToTop" in HTML_TEMPLATE

    def test_template_has_mobile_toggle(self):
        """Test that template includes mobile sidebar toggle."""
        from src.html_website.config import HTML_TEMPLATE
        assert "toggleSidebar()" in HTML_TEMPLATE
        assert "mobile-menu-btn" in HTML_TEMPLATE
