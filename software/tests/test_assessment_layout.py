"""Tests for the BIOL-1 tear-off assessment layout."""

from src.assessment_layout.main import build_tearoff_assessment


def test_build_tearoff_assessment_places_answer_sheet_and_free_response_first():
    source = """# Test

## Part A: Multiple Choice (2 points)

1. Stem one?
   - A) One
   - B) Two

2. Stem two?
   - A) One
   - B) Two

## Part B: Fill in the Blank (1 point)

1. A blank ________.

## Part C: Free Response (3 points)

1. Explain the idea.

Response space.
"""

    result = build_tearoff_assessment(source)

    assert "TEAR-OFF ANSWER SHEET" in result
    assert "1.</td>" in result and "2.</td>" in result
    assert result.index("tearoff-page") < result.index("free-response-page")
    assert result.index("free-response-page") < result.index("question-booklet-page")
    assert "## " not in result  # no raw markdown leaks into the HTML


def test_build_tearoff_assessment_preserves_questions():
    source = """# Test

## Part A: Multiple Choice (1 point)

1. What is true?
   - A) Yes

## Part B: Fill in the Blank (1 point)

1. A ________.

## Part C: Free Response (3 points)

1. Explain.
"""

    result = build_tearoff_assessment(source)

    assert result.count("What is true?") == 1
    assert "Fill in the Blank" in result and "<li>A " in result
    assert result.count("Explain.") == 1


def test_build_tearoff_assessment_reads_choose_wording():
    source = """# Test

## Part A: Multiple Choice (1 point)

1. Q?
   - A) Yes

## Part B: Fill in the Blank (1 point)

1. A ________.

## Part C: Free Response (9 points)

*Choose THREE of the following five questions.*

1. One.
2. Two.
3. Three.
4. Four.
5. Five.
"""

    result = build_tearoff_assessment(source)

    assert (
        result.count("Response 1") == 1
        and result.count("Response 2") == 1
        and result.count("Response 3") == 1
        and "Response 4" not in result
    )
    assert "One." in result and "Five." in result


def test_build_tearoff_assessment_rejects_missing_parts():
    try:
        build_tearoff_assessment("# Incomplete\n\n## Part A: Multiple Choice\n")
    except ValueError as exc:
        assert "Part B" in str(exc)
    else:
        raise AssertionError("missing assessment parts must be rejected")
