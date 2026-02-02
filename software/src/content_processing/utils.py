"""Utility functions for content processing.

Functions migrated from scripts/renumber_questions.py.
"""

import re
import logging

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
