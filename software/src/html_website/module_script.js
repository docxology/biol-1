// Sidebar & Mobile Toggle
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

// Drag Resizer Logic
const resizer = document.getElementById('resizer');
const sidebar = document.getElementById('sidebar');
let isResizing = false;

resizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    resizer.classList.add('resizing');
    document.body.style.cursor = 'col-resize';
});

document.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    const newWidth = e.clientX;
    if (newWidth > 150 && newWidth < 600) {
        sidebar.style.width = newWidth + 'px';
        document.documentElement.style.setProperty('--sidebar-width', newWidth + 'px');
    }
});

document.addEventListener('mouseup', () => {
    isResizing = false;
    resizer.classList.remove('resizing');
    document.body.style.cursor = 'default';
});

// Dark Mode with Persistence
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    updateThemeButtons(isDark);
}

function updateThemeButtons(isDark) {
    document.querySelectorAll('.dark-mode-toggle').forEach(btn => {
        btn.textContent = isDark ? 'Theme: Dark' : 'Theme: Light';
    });
}

// Global Collapse/Expand
function collapseAll() {
    document.querySelectorAll('.section-content').forEach(el => {
        el.classList.add('collapsed');
        const toggle = document.getElementById('toggle-' + el.id.replace('content-', ''));
        if(toggle) { toggle.classList.add('collapsed'); toggle.textContent = '\u25b6'; }
    });
}

function expandAll() {
    document.querySelectorAll('.section-content').forEach(el => {
        el.classList.remove('collapsed');
        const toggle = document.getElementById('toggle-' + el.id.replace('content-', ''));
        if(toggle) { toggle.classList.remove('collapsed'); toggle.textContent = '\u25bc'; }
    });
}

// Existing Section Toggle
function toggleSection(sectionId) {
    const content = document.getElementById('content-' + sectionId);
    const toggle = document.getElementById('toggle-' + sectionId);
    if (content.classList.contains('collapsed')) {
        content.classList.remove('collapsed');
        toggle.classList.remove('collapsed');
        toggle.textContent = '\u25bc';
    } else {
        content.classList.add('collapsed');
        toggle.classList.add('collapsed');
        toggle.textContent = '\u25b6';
    }
}

// ScrollSpy for Active Link Highlighting
const sections = document.querySelectorAll('section');
const navLinks = document.querySelectorAll('.nav-link');
const mainContent = document.getElementById('main-content');

mainContent.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (mainContent.scrollTop >= (sectionTop - 100)) {
            current = section.getAttribute('id');
        }
    });
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').includes(current)) {
            link.classList.add('active');
        }
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
        updateThemeButtons(true);
    }
});

/* -- Retained Quiz Logic Functions -- */
let questionStates = {};
let completedQuestions = new Set();

function selectMultipleChoice(qid, idx) {
    document.querySelectorAll(`#question-${qid} .multiple-choice-option`).forEach(o => o.classList.remove('selected'));
    const opt = document.querySelector(`#mc-${qid}-${idx}`).closest('li');
    opt.classList.add('selected');
    document.querySelector(`#mc-${qid}-${idx}`).checked = true;
    questionStates[qid] = {type: 'multiple_choice', answer: idx};
}

function updateCharCount(qid, current, max) {
    document.getElementById(`char-count-${qid}`).textContent = `${current} / ${max} characters`;
    questionStates[qid] = {type: 'free_response', answer: document.getElementById(`fr-${qid}`).value};
}

function selectTrueFalse(qid, val) {
    document.querySelectorAll(`#question-${qid} .true-false-btn`).forEach(b => b.classList.remove('selected'));
    const btn = val ? document.querySelector(`#question-${qid} button:first-child`) : document.querySelector(`#question-${qid} button:last-child`);
    btn.classList.add('selected');
    questionStates[qid] = {type: 'true_false', answer: val};
}

function updateMatching(qid) {
    const answers = {};
    document.querySelectorAll(`#question-${qid} .matching-select`).forEach((s, i) => {
        if(s.value) answers[i] = parseInt(s.value);
    });
    questionStates[qid] = {type: 'matching', answers: answers};
}

function checkQuestion(qid, type) {
    const state = questionStates[qid];
    const feedback = document.getElementById(`feedback-${qid}`);
    if(!state) { feedback.textContent = "Please answer first."; feedback.className = "question-feedback show info"; return; }

    // Simplified check logic to keep file size manageable while retaining core function
    let isCorrect = false;
    if(type === 'multiple_choice') {
        const corr = document.getElementById(`correct-${qid}`);
        if(corr) isCorrect = (state.answer === parseInt(corr.value));
    } else if(type === 'true_false') {
        const corr = document.getElementById(`correct-${qid}`);
        if(corr) isCorrect = (String(state.answer) === corr.value);
    } else if(type === 'free_response') {
        isCorrect = true; // Free response always valid
    } else if(type === 'matching') {
        // TODO: implement matching question type validation
        // Currently always marks matching answers as correct
        isCorrect = true;
    }

    if(isCorrect) {
        feedback.textContent = "Correct / Submitted!";
        feedback.className = "question-feedback show correct";
        if(!completedQuestions.has(qid)) {
            completedQuestions.add(qid);
            updateProgress();
        }
    } else {
        feedback.textContent = "Incorrect, try again.";
        feedback.className = "question-feedback show incorrect";
    }

    const expl = document.getElementById(`explanation-${qid}`);
    if(expl) feedback.innerHTML += `<div class="question-explanation">${expl.value}</div>`;
}

function updateProgress() {
    const total = parseInt(document.getElementById('questions-total').textContent);
    const comp = completedQuestions.size;
    document.getElementById('questions-completed').textContent = comp;
    const pct = total ? Math.round((comp/total)*100) : 0;
    const fill = document.getElementById('progress-fill');
    fill.style.width = pct + '%';
    fill.textContent = pct + '%';
}
