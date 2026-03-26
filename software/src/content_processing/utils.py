"""Utility functions for content processing.

Functions migrated from scripts/renumber_questions.py.
"""

import re
import logging
from typing import Any, List, Dict, Tuple

logger = logging.getLogger(__name__)


def extract_questions_from_sectioned(content: str) -> list[str]:
    """Extract all questions from a sectioned questions.md file.

    Handles format like:
    1.  **Topic Header**
        *   Question one?
        *   Question two?

    Args:
        content: The markdown content to parse

    Returns:
        List of question strings extracted from bullet points
    """
    questions = []

    # Find all bullet point questions (lines starting with * or -)
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        # Match lines that start with * or - and contain a question
        if stripped.startswith('*') or stripped.startswith('-'):
            # Remove the bullet point marker
            question = stripped.lstrip('*- \t')
            if question and len(question) > 5:  # Skip very short items
                questions.append(question)

    return questions


def format_as_continuous(questions: list[str], title: str) -> str:
    """Format questions as a continuous numbered list.

    Args:
        questions: List of question strings
        title: Title for the questions document

    Returns:
        Formatted markdown string with numbered questions
    """
    lines = [f"# {title}", ""]

    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q}")
        lines.append("")

    return '\n'.join(lines)


def normalize_whitespace(content: str) -> str:
    """Normalize whitespace in markdown content.

    - Removes trailing whitespace from lines
    - Collapses multiple blank lines into at most two
    - Ensures file ends with single newline

    Args:
        content: The markdown content to normalize

    Returns:
        Normalized markdown content
    """
    lines = content.split('\n')

    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in lines]

    # Collapse multiple blank lines
    result = []
    blank_count = 0
    for line in lines:
        if line == '':
            blank_count += 1
            if blank_count <= 2:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)

    # Ensure single trailing newline
    while result and result[-1] == '':
        result.pop()
    result.append('')

    return '\n'.join(result)


def extract_headers(content: str) -> List[Tuple[int, str]]:
    """Extract all markdown headers from content.

    Args:
        content: The markdown content to parse

    Returns:
        List of tuples (level, header_text) where level is 1-6
    """
    headers = []
    lines = content.split('\n')

    for line in lines:
        # Match markdown headers (# Header, ## Header, etc.)
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headers.append((level, text))

    return headers


def count_questions(content: str) -> Dict[str, int]:
    """Count questions in markdown content by type.

    Detects numbered questions (1. Question?), bullet questions (* Question?),
    and questions ending with ? within text.

    Args:
        content: The markdown content to analyze

    Returns:
        Dictionary with counts:
        - numbered: Questions starting with number and period
        - bulleted: Questions starting with * or -
        - inline: Lines containing ? (potential questions)
    """
    lines = content.split('\n')

    counts = {
        "numbered": 0,
        "bulleted": 0,
        "inline": 0,
    }

    for line in lines:
        stripped = line.strip()
        if re.match(r'^\d+\.', stripped):
            counts["numbered"] += 1
        elif stripped.startswith('*') or stripped.startswith('-'):
            counts["bulleted"] += 1
        elif '?' in stripped:
            counts["inline"] += 1

    return counts


def extract_numbered_items(content: str) -> List[str]:
    """Extract all numbered list items from markdown content.

    Args:
        content: The markdown content to parse

    Returns:
        List of text for each numbered item
    """
    items = []
    lines = content.split('\n')

    for line in lines:
        # Match numbered list items: "1. Text" or "12. Text"
        match = re.match(r'^\s*\d+\.\s+(.+)$', line)
        if match:
            items.append(match.group(1))

    return items


def validate_question_format(content: str) -> Dict[str, Any]:
    """Validate that a questions.md file has proper format.

    Args:
        content: The markdown content to validate

    Returns:
        Dictionary with validation results:
        - valid: bool indicating if format is correct
        - has_title: bool if file has # header
        - question_count: number of detected questions
        - issues: list of format issues found
    """
    result = {
        "valid": True,
        "has_title": False,
        "question_count": 0,
        "issues": [],
    }

    lines = content.split('\n')

    # Check for title
    for line in lines:
        if line.startswith('# '):
            result["has_title"] = True
            break

    if not result["has_title"]:
        result["issues"].append("Missing title (# Header)")
        result["valid"] = False

    # Count questions
    counts = count_questions(content)
    result["question_count"] = counts["numbered"] + counts["bulleted"]

    if result["question_count"] == 0:
        result["issues"].append("No questions found")
        result["valid"] = False

    return result

