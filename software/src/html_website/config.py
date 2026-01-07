"""Configuration for HTML website generation."""

# Default CSS for grayscale website
DEFAULT_CSS = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background-color: #2c2c2c;
    color: #fff;
    padding: 30px 20px;
    margin-bottom: 30px;
    border-radius: 5px;
}

header h1 {
    font-size: 2em;
    margin-bottom: 10px;
}

header p {
    color: #ccc;
    font-size: 1.1em;
}

section {
    background-color: #fff;
    padding: 30px;
    margin-bottom: 30px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    position: relative;
    overflow: hidden;
    min-height: 200px;
    min-width: 300px;
}

section.resizable {
    resize: both;
    overflow: auto;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    cursor: pointer;
    user-select: none;
}

.section-header h2 {
    margin: 0;
    flex: 1;
}

.section-controls {
    display: flex;
    gap: 10px;
    align-items: center;
}

.collapse-toggle {
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
    color: #666;
    padding: 5px 10px;
    transition: transform 0.3s;
}

.collapse-toggle:hover {
    color: #333;
}

.collapse-toggle.collapsed {
    transform: rotate(-90deg);
}

.section-content {
    transition: max-height 0.3s ease-out, opacity 0.3s ease-out;
    overflow: hidden;
}

.section-content.collapsed {
    max-height: 0;
    opacity: 0;
    padding: 0;
    margin: 0;
}

.resize-controls {
    display: flex;
    gap: 10px;
    margin-top: 10px;
    padding: 10px;
    background-color: #f9f9f9;
    border-radius: 3px;
}

.resize-slider {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 10px;
}

.resize-slider label {
    font-size: 0.9em;
    color: #666;
    min-width: 60px;
}

.resize-slider input[type="range"] {
    flex: 1;
    height: 5px;
    border-radius: 5px;
    background: #ddd;
    outline: none;
}

.resize-slider input[type="range"]::-webkit-slider-thumb {
    appearance: none;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: #666;
    cursor: pointer;
}

.resize-slider input[type="range"]::-moz-range-thumb {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: #666;
    cursor: pointer;
    border: none;
}

.resize-value {
    font-size: 0.9em;
    color: #666;
    min-width: 50px;
    text-align: right;
}

section h2 {
    color: #2c2c2c;
    border-bottom: 3px solid #666;
    padding-bottom: 10px;
    margin-bottom: 20px;
    font-size: 1.8em;
}

section h3 {
    color: #444;
    margin-top: 25px;
    margin-bottom: 15px;
    font-size: 1.4em;
}

section h4 {
    color: #555;
    margin-top: 20px;
    margin-bottom: 10px;
    font-size: 1.2em;
}

p {
    margin-bottom: 15px;
    color: #444;
}

ul, ol {
    margin-left: 30px;
    margin-bottom: 15px;
}

li {
    margin-bottom: 8px;
    color: #444;
}

audio {
    width: 100%;
    margin: 20px 0;
    background-color: #f0f0f0;
    border-radius: 5px;
}

.audio-section {
    background-color: #f9f9f9;
    padding: 20px;
    border-left: 4px solid #666;
    margin: 20px 0;
}

.quiz-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 5px;
    margin: 20px 0;
}

.quiz-question {
    margin-bottom: 20px;
    padding: 15px;
    background-color: #fff;
    border-left: 3px solid #666;
}

.quiz-question h4 {
    margin-top: 0;
    margin-bottom: 10px;
}

.quiz-options {
    list-style: none;
    margin-left: 0;
    margin-top: 10px;
}

.quiz-option {
    padding: 10px;
    margin: 5px 0;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.quiz-option:hover {
    background-color: #e9e9e9;
}

.quiz-option.selected {
    background-color: #d0d0d0;
    border-color: #666;
}

.quiz-option.correct {
    background-color: #c8e6c9;
    border-color: #4caf50;
}

.quiz-option.incorrect {
    background-color: #ffcdd2;
    border-color: #f44336;
}

.quiz-feedback {
    margin-top: 10px;
    padding: 10px;
    border-radius: 3px;
    display: none;
}

.quiz-feedback.show {
    display: block;
}

.quiz-feedback.correct {
    background-color: #c8e6c9;
    color: #2e7d32;
}

.quiz-feedback.incorrect {
    background-color: #ffcdd2;
    color: #c62828;
}

.check-answer-btn {
    background-color: #666;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 3px;
    cursor: pointer;
    margin-top: 10px;
    font-size: 1em;
}

.check-answer-btn:hover {
    background-color: #555;
}

.content-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
    margin: 20px 0;
}

@media (min-width: 768px) {
    .content-grid {
        grid-template-columns: 1fr 1fr;
    }
}

.code-block {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 3px;
    padding: 15px;
    overflow-x: auto;
    margin: 15px 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

table th, table td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}

table th {
    background-color: #2c2c2c;
    color: #fff;
}

table tr:nth-child(even) {
    background-color: #f9f9f9;
}

footer {
    text-align: center;
    padding: 20px;
    color: #666;
    margin-top: 40px;
}

.question-container {
    background-color: #f9f9f9;
    padding: 20px;
    margin: 20px 0;
    border-radius: 5px;
    border-left: 4px solid #666;
}

.question-header {
    display: flex;
    justify-content: space-between;
    align-items: start;
    margin-bottom: 15px;
}

.question-text {
    font-weight: 600;
    color: #2c2c2c;
    margin-bottom: 15px;
}

.question-type-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 0.75em;
    font-weight: 600;
    text-transform: uppercase;
    background-color: #666;
    color: #fff;
}

.multiple-choice-options {
    list-style: none;
    margin: 15px 0;
    padding: 0;
}

.multiple-choice-option {
    padding: 12px;
    margin: 8px 0;
    background-color: #fff;
    border: 2px solid #ddd;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.2s;
}

.multiple-choice-option:hover {
    background-color: #f0f0f0;
    border-color: #999;
}

.multiple-choice-option input[type="radio"] {
    margin-right: 10px;
}

.multiple-choice-option.selected {
    background-color: #e3f2fd;
    border-color: #2196f3;
}

.multiple-choice-option.correct {
    background-color: #c8e6c9;
    border-color: #4caf50;
}

.multiple-choice-option.incorrect {
    background-color: #ffcdd2;
    border-color: #f44336;
}

.free-response-textarea {
    width: 100%;
    min-height: 150px;
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-family: inherit;
    font-size: 1em;
    resize: vertical;
    margin: 10px 0;
}

.free-response-textarea:focus {
    outline: none;
    border-color: #666;
}

.char-count {
    font-size: 0.9em;
    color: #666;
    text-align: right;
    margin-top: 5px;
}

.true-false-buttons {
    display: flex;
    gap: 15px;
    margin: 15px 0;
}

.true-false-btn {
    flex: 1;
    padding: 15px 30px;
    border: 2px solid #ddd;
    border-radius: 5px;
    background-color: #fff;
    cursor: pointer;
    font-size: 1.1em;
    font-weight: 600;
    transition: all 0.2s;
}

.true-false-btn:hover {
    background-color: #f0f0f0;
    border-color: #999;
}

.true-false-btn.selected {
    background-color: #e3f2fd;
    border-color: #2196f3;
}

.true-false-btn.correct {
    background-color: #c8e6c9;
    border-color: #4caf50;
}

.true-false-btn.incorrect {
    background-color: #ffcdd2;
    border-color: #f44336;
}

.matching-container {
    margin: 15px 0;
}

.matching-pairs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin: 15px 0;
}

.matching-item {
    padding: 12px;
    background-color: #fff;
    border: 2px solid #ddd;
    border-radius: 5px;
}

.matching-term {
    font-weight: 600;
    margin-bottom: 8px;
    color: #2c2c2c;
}

.matching-select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 3px;
    font-family: inherit;
}

.matching-select:focus {
    outline: none;
    border-color: #666;
}

.question-feedback {
    margin-top: 15px;
    padding: 12px;
    border-radius: 5px;
    display: none;
}

.question-feedback.show {
    display: block;
}

.question-feedback.correct {
    background-color: #c8e6c9;
    color: #2e7d32;
    border-left: 4px solid #4caf50;
}

.question-feedback.incorrect {
    background-color: #ffcdd2;
    color: #c62828;
    border-left: 4px solid #f44336;
}

.question-feedback.info {
    background-color: #e3f2fd;
    color: #1976d2;
    border-left: 4px solid #2196f3;
}

.question-explanation {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid rgba(0,0,0,0.1);
    font-style: italic;
}

.check-question-btn {
    background-color: #666;
    color: #fff;
    border: none;
    padding: 12px 24px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    font-weight: 600;
    margin-top: 15px;
    transition: background-color 0.2s;
}

.check-question-btn:hover {
    background-color: #555;
}

.check-question-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.questions-progress {
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 20px;
}

.progress-bar {
    width: 100%;
    height: 20px;
    background-color: #ddd;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 10px;
}

.progress-fill {
    height: 100%;
    background-color: #4caf50;
    transition: width 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 0.8em;
    font-weight: 600;
}
"""

# HTML template structure
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css}
    </style>
</head>
<body>
    <header>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </header>
    
    {content}
    
    <footer>
        <p>Generated for {course_name}</p>
    </footer>
    
    <script>
{javascript}
    </script>
</body>
</html>
"""
