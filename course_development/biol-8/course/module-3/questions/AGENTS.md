# Module 1 Questions Technical Documentation

## Overview

Technical documentation for question format, structure, and processing for Module 1.

## Question Format

Questions are stored in JSON format with the following structure:

```json
{
  "questions": [
    {
      "id": "unique-question-id",
      "type": "multiple_choice|free_response|true_false|matching",
      "question": "Question text",
      ...
    }
  ]
}
```

## Question Types

### Multiple Choice

```json
{
  "id": "q1",
  "type": "multiple_choice",
  "question": "Question text",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "correct": 0,
  "explanation": "Explanation of correct answer"
}
```

- `options`: Array of answer choices
- `correct`: Index (0-based) of correct answer
- `explanation`: Optional explanation shown after answer

### Free Response

```json
{
  "id": "q2",
  "type": "free_response",
  "question": "Question text",
  "placeholder": "Optional placeholder text",
  "max_length": 500
}
```

- `placeholder`: Optional placeholder text for textarea
- `max_length`: Optional maximum character count

### True/False

```json
{
  "id": "q3",
  "type": "true_false",
  "question": "Question text",
  "correct": true,
  "explanation": "Explanation of answer"
}
```

- `correct`: Boolean value (true or false)
- `explanation`: Optional explanation

### Matching

```json
{
  "id": "q4",
  "type": "matching",
  "question": "Match the terms with definitions",
  "items": [
    {"term": "Term 1", "definition": "Definition 1"},
    {"term": "Term 2", "definition": "Definition 2"}
  ]
}
```

- `items`: Array of term-definition pairs to match

## Processing

Questions are processed by the HTML website generation module:

- **Module**: `software/src/html_website/main.py`
- **Function**: `generate_module_website()`
- **Utility**: `parse_questions_json()` from `html_website/utils.py`

## Output

Questions are rendered as interactive HTML elements on the module website with:
- Answer validation
- Feedback and explanations
- Progress tracking
- State persistence
