"""Main functions for HTML website generation."""

from pathlib import Path
from typing import Dict, List, Optional

from . import config
from ..batch_processing.logging_config import get_logger
from .utils import (
    ensure_output_directory,
    extract_quiz_questions,
    find_audio_file,
    find_questions_file,
    find_text_file,
    get_relative_path,
    markdown_to_html,
    parse_questions_json,
    read_markdown_file,
)

logger = get_logger("html_website")


def generate_module_website(
    module_path: str,
    output_dir: Optional[str] = None,
    course_name: Optional[str] = None,
) -> str:
    """Generate HTML website for a module.

    Args:
        module_path: Path to module directory
        output_dir: Output directory (defaults to module_path/output/website)
        course_name: Course name for display (optional)

    Returns:
        Path to generated HTML file

    Raises:
        ValueError: If module path doesn't exist
        OSError: If website generation fails
    """
    module_dir = Path(module_path)
    if not module_dir.exists():
        raise ValueError(f"Module path does not exist: {module_path}")

    logger.info(f"Generating website for module: {module_dir.name}")

    # Determine output directory
    if output_dir:
        website_output = Path(output_dir)
    else:
        website_output = module_dir / "output" / "website"

    ensure_output_directory(website_output)

    # Get module name
    module_name = module_dir.name
    if not course_name:
        # Try to extract course name from parent path
        course_name = "BIOL-1"

    # Curriculum element types and their source files
    curriculum_elements = {
        "lecture-content": {
            "source_pattern": "sample_lecture-content.md",
            "title": "Lecture Content",
        },
        "lab-protocols": {
            "source_pattern": "sample_lab-protocol.md",
            "title": "Lab Protocol",
        },
        "study-guides": {
            "source_pattern": "sample_study-guide.md",
            "title": "Study Guide",
        },
    }

    # Build website content
    content_sections = []

    # Process each curriculum element
    for element_type, element_info in curriculum_elements.items():
        source_file = module_dir / element_info["source_pattern"]
        if not source_file.exists():
            continue

        # Read markdown content
        markdown_content = read_markdown_file(source_file)
        html_content = markdown_to_html(markdown_content)

        # Find audio and text files
        base_name = source_file.stem
        output_base = module_dir / "output"
        audio_file = find_audio_file(base_name, output_base, element_type)
        text_file = find_text_file(base_name, output_base, element_type)

        # Build section HTML with collapsible header and resize controls
        section_id = element_type.replace("-", "_")
        section_html = f'<section id="{section_id}" class="resizable">\n'
        section_html += '<div class="section-header" onclick="toggleSection(\'' + section_id + '\')">\n'
        section_html += f'<h2>{element_info["title"]}</h2>\n'
        section_html += '<div class="section-controls">\n'
        section_html += f'<button class="collapse-toggle" id="toggle-{section_id}" aria-label="Toggle section">▼</button>\n'
        section_html += '</div>\n'
        section_html += '</div>\n'
        section_html += '<div class="section-content" id="content-' + section_id + '">\n'

        # Add audio player if available
        if audio_file:
            audio_rel_path = get_relative_path(audio_file, website_output)
            section_html += '<div class="audio-section">\n'
            section_html += '<h3>Audio Version</h3>\n'
            section_html += f'<audio controls><source src="{audio_rel_path}" type="audio/mpeg">Your browser does not support the audio element.</audio>\n'
            section_html += "</div>\n"

        # Add text content
        section_html += '<div class="content-grid">\n'
        section_html += "<div>\n"
        section_html += html_content
        section_html += "</div>\n"

        # Add plain text version if available
        if text_file:
            text_content = text_file.read_text(encoding="utf-8")
            text_rel_path = get_relative_path(text_file, website_output)
            section_html += '<div>\n'
            section_html += '<h3>Plain Text Version</h3>\n'
            section_html += '<div class="code-block">\n'
            section_html += f'<pre>{text_content[:500]}...</pre>\n'
            section_html += f'<p><a href="{text_rel_path}" download>Download Full Text</a></p>\n'
            section_html += "</div>\n"
            section_html += "</div>\n"

        section_html += "</div>\n"
        section_html += '<div class="resize-controls">\n'
        section_html += '<div class="resize-slider">\n'
        section_html += '<label>Width:</label>\n'
        section_html += f'<input type="range" id="width-{section_id}" min="300" max="1000" value="100" oninput="resizeSection(\'{section_id}\', \'width\', this.value)">\n'
        section_html += f'<span class="resize-value" id="width-value-{section_id}">100%</span>\n'
        section_html += '</div>\n'
        section_html += '<div class="resize-slider">\n'
        section_html += '<label>Height:</label>\n'
        section_html += f'<input type="range" id="height-{section_id}" min="200" max="800" value="100" oninput="resizeSection(\'{section_id}\', \'height\', this.value)">\n'
        section_html += f'<span class="resize-value" id="height-value-{section_id}">100%</span>\n'
        section_html += '</div>\n'
        section_html += '</div>\n'
        section_html += '</div>\n'
        section_html += "</section>\n"

        content_sections.append(section_html)

    # Process assignments
    assignments_dir = module_dir / "assignments"
    if assignments_dir.exists():
        assignment_files = list(assignments_dir.glob("*.md"))
        if assignment_files:
            assignments_html = '<section id="assignments" class="resizable">\n'
            assignments_html += '<div class="section-header" onclick="toggleSection(\'assignments\')">\n'
            assignments_html += "<h2>Assignments</h2>\n"
            assignments_html += '<div class="section-controls">\n'
            assignments_html += '<button class="collapse-toggle" id="toggle-assignments" aria-label="Toggle section">▼</button>\n'
            assignments_html += '</div>\n'
            assignments_html += '</div>\n'
            assignments_html += '<div class="section-content" id="content-assignments">\n'

            for assignment_file in sorted(assignment_files):
                markdown_content = read_markdown_file(assignment_file)
                html_content = markdown_to_html(markdown_content)

                base_name = assignment_file.stem
                output_base = module_dir / "output"
                audio_file = find_audio_file(base_name, output_base, "assignments")

                assignments_html += f'<div class="assignment-item">\n'
                assignments_html += html_content

                if audio_file:
                    audio_rel_path = get_relative_path(audio_file, website_output)
                    assignments_html += '<div class="audio-section">\n'
                    assignments_html += '<h4>Audio Version</h4>\n'
                    assignments_html += f'<audio controls><source src="{audio_rel_path}" type="audio/mpeg">Your browser does not support the audio element.</audio>\n'
                    assignments_html += "</div>\n"

                assignments_html += "</div>\n"
                assignments_html += "<hr style='margin: 30px 0; border: none; border-top: 1px solid #ddd;'>\n"

            assignments_html += '<div class="resize-controls">\n'
            assignments_html += '<div class="resize-slider">\n'
            assignments_html += '<label>Width:</label>\n'
            assignments_html += '<input type="range" id="width-assignments" min="300" max="1000" value="100" oninput="resizeSection(\'assignments\', \'width\', this.value)">\n'
            assignments_html += '<span class="resize-value" id="width-value-assignments">100%</span>\n'
            assignments_html += '</div>\n'
            assignments_html += '<div class="resize-slider">\n'
            assignments_html += '<label>Height:</label>\n'
            assignments_html += '<input type="range" id="height-assignments" min="200" max="800" value="100" oninput="resizeSection(\'assignments\', \'height\', this.value)">\n'
            assignments_html += '<span class="resize-value" id="height-value-assignments">100%</span>\n'
            assignments_html += '</div>\n'
            assignments_html += '</div>\n'
            assignments_html += '</div>\n'
            assignments_html += "</section>\n"
            content_sections.append(assignments_html)

    # Process questions from JSON file
    questions_file = find_questions_file(module_dir)
    if questions_file:
        try:
            questions = parse_questions_json(questions_file)
            if questions:
                questions_html = '<section id="questions" class="resizable">\n'
                questions_html += '<div class="section-header" onclick="toggleSection(\'questions\')">\n'
                questions_html += "<h2>Interactive Questions</h2>\n"
                questions_html += '<div class="section-controls">\n'
                questions_html += '<button class="collapse-toggle" id="toggle-questions" aria-label="Toggle section">▼</button>\n'
                questions_html += '</div>\n'
                questions_html += '</div>\n'
                questions_html += '<div class="section-content" id="content-questions">\n'
                questions_html += '<div class="questions-progress">\n'
                questions_html += '<p><strong>Progress:</strong> <span id="questions-completed">0</span> / <span id="questions-total">' + str(len(questions)) + '</span> completed</p>\n'
                questions_html += '<div class="progress-bar"><div class="progress-fill" id="progress-fill" style="width: 0%">0%</div></div>\n'
                questions_html += '</div>\n'

                for idx, question in enumerate(questions, 1):
                    q_id = question.get("id", f"q{idx}")
                    q_type = question.get("type", "free_response")
                    q_text = question.get("question", "")
                    
                    questions_html += f'<div class="question-container" id="question-{q_id}">\n'
                    questions_html += '<div class="question-header">\n'
                    questions_html += f'<div class="question-text">Question {idx}: {q_text}</div>\n'
                    questions_html += f'<span class="question-type-badge">{q_type.replace("_", " ")}</span>\n'
                    questions_html += '</div>\n'

                    if q_type == "multiple_choice":
                        options = question.get("options", [])
                        questions_html += '<ul class="multiple-choice-options">\n'
                        for opt_idx, option in enumerate(options):
                            questions_html += f'<li class="multiple-choice-option" onclick="selectMultipleChoice(\'{q_id}\', {opt_idx})">\n'
                            questions_html += f'<input type="radio" name="mc-{q_id}" id="mc-{q_id}-{opt_idx}" value="{opt_idx}">\n'
                            questions_html += f'<label for="mc-{q_id}-{opt_idx}">{option}</label>\n'
                            questions_html += '</li>\n'
                        questions_html += '</ul>\n'
                        correct_answer = question.get("correct")
                        if correct_answer is not None:
                            questions_html += f'<input type="hidden" id="correct-{q_id}" value="{correct_answer}">\n'

                    elif q_type == "free_response":
                        placeholder = question.get("placeholder", "")
                        max_length = question.get("max_length", 1000)
                        questions_html += f'<textarea class="free-response-textarea" id="fr-{q_id}" placeholder="{placeholder}" maxlength="{max_length}" oninput="updateCharCount(\'{q_id}\', this.value.length, {max_length})"></textarea>\n'
                        questions_html += f'<div class="char-count" id="char-count-{q_id}">0 / {max_length} characters</div>\n'

                    elif q_type == "true_false":
                        questions_html += '<div class="true-false-buttons">\n'
                        questions_html += f'<button class="true-false-btn" onclick="selectTrueFalse(\'{q_id}\', true)">True</button>\n'
                        questions_html += f'<button class="true-false-btn" onclick="selectTrueFalse(\'{q_id}\', false)">False</button>\n'
                        questions_html += '</div>\n'
                        correct_answer = question.get("correct")
                        if correct_answer is not None:
                            questions_html += f'<input type="hidden" id="correct-{q_id}" value="{str(correct_answer).lower()}">\n'

                    elif q_type == "matching":
                        items = question.get("items", [])
                        questions_html += '<div class="matching-container">\n'
                        questions_html += '<div class="matching-pairs">\n'
                        for item_idx, item in enumerate(items):
                            term = item.get("term", "")
                            definition = item.get("definition", "")
                            questions_html += '<div class="matching-item">\n'
                            questions_html += f'<div class="matching-term">{term}</div>\n'
                            questions_html += f'<select class="matching-select" id="match-{q_id}-{item_idx}" onchange="updateMatching(\'{q_id}\')">\n'
                            questions_html += '<option value="">Select definition...</option>\n'
                            for def_idx, def_item in enumerate(items):
                                questions_html += f'<option value="{def_idx}">{def_item.get("definition", "")}</option>\n'
                            questions_html += '</select>\n'
                            questions_html += f'<input type="hidden" id="correct-match-{q_id}-{item_idx}" value="{item_idx}">\n'
                            questions_html += '</div>\n'
                        questions_html += '</div>\n'
                        questions_html += '</div>\n'

                    explanation = question.get("explanation", "")
                    if explanation:
                        questions_html += f'<input type="hidden" id="explanation-{q_id}" value="{explanation}">\n'

                    questions_html += f'<button class="check-question-btn" onclick="checkQuestion(\'{q_id}\', \'{q_type}\')">Check Answer</button>\n'
                    questions_html += f'<div class="question-feedback" id="feedback-{q_id}"></div>\n'
                    questions_html += '</div>\n'

                questions_html += '<div class="resize-controls">\n'
                questions_html += '<div class="resize-slider">\n'
                questions_html += '<label>Width:</label>\n'
                questions_html += '<input type="range" id="width-questions" min="300" max="1000" value="100" oninput="resizeSection(\'questions\', \'width\', this.value)">\n'
                questions_html += '<span class="resize-value" id="width-value-questions">100%</span>\n'
                questions_html += '</div>\n'
                questions_html += '<div class="resize-slider">\n'
                questions_html += '<label>Height:</label>\n'
                questions_html += '<input type="range" id="height-questions" min="200" max="800" value="100" oninput="resizeSection(\'questions\', \'height\', this.value)">\n'
                questions_html += '<span class="resize-value" id="height-value-questions">100%</span>\n'
                questions_html += '</div>\n'
                questions_html += '</div>\n'
                questions_html += '</div>\n'
                questions_html += "</section>\n"
                content_sections.append(questions_html)
        except Exception as e:
            # If questions file exists but can't be parsed, continue without questions
            pass

    # Combine all content
    full_content = "\n".join(content_sections)

    # Generate JavaScript for all interactivity
    javascript = """
    // Section collapse/expand functionality
    function toggleSection(sectionId) {
        const content = document.getElementById('content-' + sectionId);
        const toggle = document.getElementById('toggle-' + sectionId);
        
        if (content.classList.contains('collapsed')) {
            content.classList.remove('collapsed');
            toggle.classList.remove('collapsed');
            toggle.textContent = '▼';
            localStorage.setItem('section-' + sectionId, 'expanded');
        } else {
            content.classList.add('collapsed');
            toggle.classList.add('collapsed');
            toggle.textContent = '▶';
            localStorage.setItem('section-' + sectionId, 'collapsed');
        }
    }

    // Restore section states from localStorage
    function restoreSectionStates() {
        document.querySelectorAll('.section-content').forEach(content => {
            const sectionId = content.id.replace('content-', '');
            const state = localStorage.getItem('section-' + sectionId);
            if (state === 'collapsed') {
                content.classList.add('collapsed');
                const toggle = document.getElementById('toggle-' + sectionId);
                if (toggle) {
                    toggle.classList.add('collapsed');
                    toggle.textContent = '▶';
                }
            }
        });
    }

    // Resize section functionality
    function resizeSection(sectionId, dimension, value) {
        const section = document.getElementById(sectionId);
        const valueDisplay = document.getElementById(dimension + '-value-' + sectionId);
        
        if (dimension === 'width') {
            const width = 300 + (value / 100) * 700; // 300-1000px range
            section.style.width = width + 'px';
            valueDisplay.textContent = Math.round(width) + 'px';
            localStorage.setItem('section-' + sectionId + '-width', width);
        } else if (dimension === 'height') {
            const height = 200 + (value / 100) * 600; // 200-800px range
            section.style.height = height + 'px';
            valueDisplay.textContent = Math.round(height) + 'px';
            localStorage.setItem('section-' + sectionId + '-height', height);
        }
    }

    // Restore resize preferences from localStorage
    function restoreResizePreferences() {
        document.querySelectorAll('.resizable').forEach(section => {
            const sectionId = section.id;
            const savedWidth = localStorage.getItem('section-' + sectionId + '-width');
            const savedHeight = localStorage.getItem('section-' + sectionId + '-height');
            
            if (savedWidth) {
                section.style.width = savedWidth + 'px';
                const widthSlider = document.getElementById('width-' + sectionId);
                const widthValue = document.getElementById('width-value-' + sectionId);
                if (widthSlider && widthValue) {
                    const sliderValue = ((parseFloat(savedWidth) - 300) / 700) * 100;
                    widthSlider.value = sliderValue;
                    widthValue.textContent = Math.round(savedWidth) + 'px';
                }
            }
            
            if (savedHeight) {
                section.style.height = savedHeight + 'px';
                const heightSlider = document.getElementById('height-' + sectionId);
                const heightValue = document.getElementById('height-value-' + sectionId);
                if (heightSlider && heightValue) {
                    const sliderValue = ((parseFloat(savedHeight) - 200) / 600) * 100;
                    heightSlider.value = sliderValue;
                    heightValue.textContent = Math.round(savedHeight) + 'px';
                }
            }
        });
    }

    // Question state tracking
    let questionStates = {};
    let completedQuestions = new Set();

    // Multiple choice question handling
    function selectMultipleChoice(questionId, optionIndex) {
        const options = document.querySelectorAll('#question-' + questionId + ' .multiple-choice-option');
        options.forEach(opt => opt.classList.remove('selected'));
        
        const selectedOption = document.querySelector(`#mc-${questionId}-${optionIndex}`).closest('.multiple-choice-option');
        selectedOption.classList.add('selected');
        document.querySelector(`#mc-${questionId}-${optionIndex}`).checked = true;
        
        questionStates[questionId] = { type: 'multiple_choice', answer: optionIndex };
    }

    // Free response question handling
    function updateCharCount(questionId, current, max) {
        const charCount = document.getElementById('char-count-' + questionId);
        if (charCount) {
            charCount.textContent = current + ' / ' + max + ' characters';
        }
        
        const textarea = document.getElementById('fr-' + questionId);
        if (textarea && textarea.value.trim()) {
            questionStates[questionId] = { type: 'free_response', answer: textarea.value };
        }
    }

    // True/False question handling
    function selectTrueFalse(questionId, value) {
        const buttons = document.querySelectorAll('#question-' + questionId + ' .true-false-btn');
        buttons.forEach(btn => btn.classList.remove('selected'));
        
        const selectedBtn = value ? buttons[0] : buttons[1];
        selectedBtn.classList.add('selected');
        
        questionStates[questionId] = { type: 'true_false', answer: value };
    }

    // Matching question handling
    function updateMatching(questionId) {
        questionStates[questionId] = { type: 'matching', answers: {} };
        const selects = document.querySelectorAll('#question-' + questionId + ' .matching-select');
        selects.forEach((select, idx) => {
            if (select.value !== '') {
                questionStates[questionId].answers[idx] = parseInt(select.value);
            }
        });
    }

    // Check question answer
    function checkQuestion(questionId, questionType) {
        const feedback = document.getElementById('feedback-' + questionId);
        const state = questionStates[questionId];
        
        if (!state || (questionType !== 'free_response' && state.answer === undefined && (!state.answers || Object.keys(state.answers).length === 0))) {
            feedback.textContent = 'Please provide an answer first.';
            feedback.className = 'question-feedback show info';
            return;
        }

        let isCorrect = false;
        let explanation = '';

        if (questionType === 'multiple_choice') {
            const correctAnswer = document.getElementById('correct-' + questionId);
            if (correctAnswer) {
                const correct = parseInt(correctAnswer.value);
                isCorrect = state.answer === correct;
                
                const options = document.querySelectorAll('#question-' + questionId + ' .multiple-choice-option');
                options.forEach((opt, idx) => {
                    opt.classList.remove('correct', 'incorrect');
                    if (idx === correct) {
                        opt.classList.add('correct');
                    } else if (idx === state.answer && !isCorrect) {
                        opt.classList.add('incorrect');
                    }
                });
            }
        } else if (questionType === 'true_false') {
            const correctAnswer = document.getElementById('correct-' + questionId);
            if (correctAnswer) {
                const correct = correctAnswer.value === 'true';
                isCorrect = state.answer === correct;
                
                const buttons = document.querySelectorAll('#question-' + questionId + ' .true-false-btn');
                buttons.forEach((btn, idx) => {
                    btn.classList.remove('correct', 'incorrect');
                    const btnValue = idx === 0;
                    if (btnValue === correct) {
                        btn.classList.add('correct');
                    } else if (btnValue === state.answer && !isCorrect) {
                        btn.classList.add('incorrect');
                    }
                });
            }
        } else if (questionType === 'matching') {
            let allCorrect = true;
            const selects = document.querySelectorAll('#question-' + questionId + ' .matching-select');
            selects.forEach((select, idx) => {
                const correctInput = document.getElementById('correct-match-' + questionId + '-' + idx);
                if (correctInput) {
                    const correct = parseInt(correctInput.value);
                    const selected = select.value !== '' ? parseInt(select.value) : -1;
                    if (selected === correct) {
                        select.style.borderColor = '#4caf50';
                    } else {
                        select.style.borderColor = '#f44336';
                        allCorrect = false;
                    }
                }
            });
            isCorrect = allCorrect && Object.keys(state.answers || {}).length === selects.length;
        } else if (questionType === 'free_response') {
            // Free response is always considered "answered" for progress tracking
            isCorrect = true; // For progress purposes
            feedback.textContent = 'Answer submitted. Review your response and compare with course materials.';
            feedback.className = 'question-feedback show info';
            
            const explanationEl = document.getElementById('explanation-' + questionId);
            if (explanationEl) {
                feedback.innerHTML += '<div class="question-explanation">' + explanationEl.value + '</div>';
            }
            
            updateProgress();
            return;
        }

        const explanationEl = document.getElementById('explanation-' + questionId);
        if (explanationEl) {
            explanation = explanationEl.value;
        }

        if (isCorrect) {
            feedback.textContent = 'Correct!';
            feedback.className = 'question-feedback show correct';
            if (explanation) {
                feedback.innerHTML += '<div class="question-explanation">' + explanation + '</div>';
            }
            completedQuestions.add(questionId);
        } else {
            feedback.textContent = 'Incorrect. Please try again.';
            feedback.className = 'question-feedback show incorrect';
            if (explanation) {
                feedback.innerHTML += '<div class="question-explanation">' + explanation + '</div>';
            }
        }

        updateProgress();
    }

    // Update progress bar
    function updateProgress() {
        const totalEl = document.getElementById('questions-total');
        if (!totalEl) return;
        
        const total = parseInt(totalEl.textContent);
        const completed = completedQuestions.size;
        
        document.getElementById('questions-completed').textContent = completed;
        const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
        
        const progressFill = document.getElementById('progress-fill');
        if (progressFill) {
            progressFill.style.width = percentage + '%';
            progressFill.textContent = percentage + '%';
        }
    }

    // Initialize on page load
    document.addEventListener('DOMContentLoaded', function() {
        restoreSectionStates();
        restoreResizePreferences();
        
        // Load saved question states
        const savedStates = localStorage.getItem('questionStates');
        if (savedStates) {
            try {
                questionStates = JSON.parse(savedStates);
            } catch (e) {
                questionStates = {};
            }
        }
        
        const savedCompleted = localStorage.getItem('completedQuestions');
        if (savedCompleted) {
            try {
                completedQuestions = new Set(JSON.parse(savedCompleted));
                updateProgress();
            } catch (e) {
                completedQuestions = new Set();
            }
        }
    });

    // Save question states periodically
    setInterval(function() {
        localStorage.setItem('questionStates', JSON.stringify(questionStates));
        localStorage.setItem('completedQuestions', JSON.stringify(Array.from(completedQuestions)));
    }, 2000);
    """

    # Generate final HTML
    title = f"{module_name.replace('-', ' ').title()}"
    subtitle = f"Complete module materials for {course_name}"

    html_output = config.HTML_TEMPLATE.format(
        title=title,
        subtitle=subtitle,
        course_name=course_name,
        css=config.DEFAULT_CSS,
        content=full_content,
        javascript=javascript,
    )

    # Write HTML file
    html_file = website_output / "index.html"
    html_file.write_text(html_output, encoding="utf-8")

    logger.info(f"Website generated: {html_file}")
    logger.debug(f"Website size: {len(html_output)} bytes")

    return str(html_file)
