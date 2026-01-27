"""Configuration constants for lab manual rendering."""

from typing import Any, Dict, List

# Lab manual-specific CSS for print-friendly, fillable worksheets
LAB_MANUAL_CSS = """
/* Lab Manual Worksheet Styles */
@page {
    size: letter;
    margin: 0.75in;
}

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #1a1a1a;
}

h1 {
    font-size: 18pt;
    font-weight: bold;
    text-align: center;
    margin-bottom: 0.5em;
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
}

h2 {
    font-size: 14pt;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: #2c5aa0;
}

h3 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 1em;
    margin-bottom: 0.3em;
}

/* Lab Header Info */
.lab-header {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1em;
    margin-bottom: 1.5em;
    padding: 1em;
    border: 1px solid #ccc;
    background-color: #f9f9f9;
}

.lab-header-field {
    display: flex;
    align-items: baseline;
    gap: 0.5em;
}

.lab-header-label {
    font-weight: bold;
    white-space: nowrap;
}

.lab-header-value {
    flex: 1;
    border-bottom: 1px solid #333;
    min-height: 1.5em;
}

/* Data Tables */
.lab-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
}

.lab-table th {
    background-color: #e8e8e8;
    font-weight: bold;
    text-align: left;
    padding: 8px 12px;
    border: 1px solid #333;
}

.lab-table td {
    padding: 8px 12px;
    border: 1px solid #333;
    min-height: 2em;
    vertical-align: top;
}

.lab-table td.fillable {
    background-color: #fffef0;
    min-height: 2.5em;
}

.lab-table tr:nth-child(even) {
    background-color: #f5f5f5;
}

/* Fillable Fields */
.fill-text {
    display: inline-block;
    min-width: 200px;
    border-bottom: 1px solid #333;
    padding: 2px 4px;
    background-color: #fffef0;
}

.fill-textarea {
    display: block;
    width: 100%;
    min-height: 3em;
    border: 1px solid #333;
    padding: 8px;
    margin: 0.5em 0;
    background-color: #fffef0;
}

.fill-checkbox {
    display: flex;
    align-items: flex-start;
    gap: 0.5em;
    margin: 0.3em 0;
}

.fill-checkbox input[type="checkbox"] {
    width: 1em;
    height: 1em;
    margin-top: 0.25em;
}

/* Measurement Table */
.measurement-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
}

.measurement-table th {
    background-color: #2c5aa0;
    color: white;
    font-weight: bold;
    text-align: center;
    padding: 10px 12px;
    border: 1px solid #1a3d6d;
}

.measurement-table td {
    padding: 12px;
    border: 1px solid #333;
    text-align: center;
}

.measurement-table td.fillable {
    background-color: #fffef0;
    min-height: 3em;
}

.measurement-table .row-number {
    width: 40px;
    background-color: #e8e8e8;
    font-weight: bold;
}

/* Object Selection Section */
.object-selection {
    margin: 1em 0;
    padding: 1em;
    border: 2px solid #2c5aa0;
    border-radius: 8px;
    background-color: #f0f5ff;
}

.object-selection h3 {
    margin-top: 0;
    color: #2c5aa0;
}

.object-field {
    display: flex;
    align-items: baseline;
    gap: 0.5em;
    margin: 1em 0;
}

.object-label {
    font-weight: bold;
    min-width: 150px;
}

.object-input {
    flex: 1;
    border-bottom: 2px solid #333;
    min-height: 1.5em;
    background-color: #fffef0;
    padding: 4px;
}

/* Feasibility Section */
.feasibility-section {
    margin: 1em 0;
    padding: 1em;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.feasibility-question {
    font-weight: bold;
    margin-bottom: 0.5em;
}

.feasibility-options {
    margin-left: 1em;
}

/* Reflection Box */
.reflection-box {
    margin: 1em 0;
    padding: 1em;
    border: 2px dashed #666;
    background-color: #fafafa;
    min-height: 100px;
}

/* Print Styles */
@media print {
    .lab-table td.fillable,
    .fill-text,
    .fill-textarea,
    .object-input {
        background-color: white !important;
    }
    
    .no-print {
        display: none !important;
    }
    
    h1, h2, h3 {
        page-break-after: avoid;
    }
    
    .lab-table, .measurement-table {
        page-break-inside: avoid;
    }
}
"""

# HTML template for lab manual
LAB_HTML_TEMPLATE = """<!DOCTYPE html>
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
    <div class="lab-manual">
        {content}
    </div>
    <script>
{javascript}
    </script>
</body>
</html>
"""

# Default PDF generation options
DEFAULT_PDF_OPTIONS: Dict[str, Any] = {
    "page_size": "letter",
    "margin_top": "0.75in",
    "margin_bottom": "0.75in",
    "margin_left": "0.75in",
    "margin_right": "0.75in",
}

# Lab element directive patterns
LAB_DIRECTIVES = {
    "data-table": r"<!-- lab:data-table(.*)-->(.*)<!-- /lab:data-table -->",
    "object-selection": r"<!-- lab:object-selection -->(.*)<!-- /lab:object-selection -->",
    "measurement-feasibility": r"<!-- lab:measurement-feasibility -->(.*)<!-- /lab:measurement-feasibility -->",
    "reflection": r"<!-- lab:reflection -->(.*)<!-- /lab:reflection -->",
}

# Default measurement table columns
DEFAULT_MEASUREMENT_COLUMNS: List[str] = [
    "Physical Aspect",
    "Measurement Device",
    "Measurement Unit",
]

# Default number of rows for data tables
DEFAULT_TABLE_ROWS = 5

# Interactive JavaScript for HTML output
LAB_INTERACTIVE_JS = """
// Lab Manual Interactive Functions

// Auto-save form data to localStorage
function saveLabData() {
    const form = document.querySelector('.lab-manual');
    const inputs = form.querySelectorAll('input, textarea');
    const data = {};
    inputs.forEach((input, idx) => {
        const key = input.id || input.name || `field_${idx}`;
        if (input.type === 'checkbox') {
            data[key] = input.checked;
        } else {
            data[key] = input.value;
        }
    });
    localStorage.setItem('labManualData_' + document.title, JSON.stringify(data));
    showSaveNotification();
}

// Load saved form data
function loadLabData() {
    const saved = localStorage.getItem('labManualData_' + document.title);
    if (saved) {
        const data = JSON.parse(saved);
        const form = document.querySelector('.lab-manual');
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach((input, idx) => {
            const key = input.id || input.name || `field_${idx}`;
            if (data[key] !== undefined) {
                if (input.type === 'checkbox') {
                    input.checked = data[key];
                } else {
                    input.value = data[key];
                }
            }
        });
    }
}

// Show save notification
function showSaveNotification() {
    let notification = document.getElementById('save-notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'save-notification';
        notification.style.cssText = 'position: fixed; bottom: 20px; right: 20px; background: #2c5aa0; color: white; padding: 10px 20px; border-radius: 4px; opacity: 0; transition: opacity 0.3s;';
        document.body.appendChild(notification);
    }
    notification.textContent = 'Progress saved!';
    notification.style.opacity = '1';
    setTimeout(() => { notification.style.opacity = '0'; }, 2000);
}

// Clear all data
function clearLabData() {
    if (confirm('Clear all entered data? This cannot be undone.')) {
        localStorage.removeItem('labManualData_' + document.title);
        location.reload();
    }
}

// Print lab manual
function printLabManual() {
    window.print();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadLabData();
    
    // Auto-save on input
    const form = document.querySelector('.lab-manual');
    if (form) {
        form.addEventListener('input', () => {
            clearTimeout(window.saveTimeout);
            window.saveTimeout = setTimeout(saveLabData, 1000);
        });
    }
});
"""
