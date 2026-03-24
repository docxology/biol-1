# Dashboard Format Guide

> **Navigation**: [← Lab Format](LAB_FORMAT.md) | [README](README.md) | [Architecture](ARCHITECTURE.md) | [Output HTML](OUTPUT_HTML.md)

Complete guide for building interactive lab dashboards. Dashboards are standalone HTML pages with Canvas-based visualizations, simulations, and interactive learning tools that complement each lab protocol.

---

## File Naming & Location

| Convention | Example |
|-----------|---------|
| **Pattern** | `lab-XX_topic-dashboard.html` |
| **Location** | `course_development/biol-8/course/labs/dashboards/` |
| **Companion Lab** | `course/labs/lab-XX_topic.md` |

Every dashboard corresponds 1:1 with a lab protocol file. Some labs have multiple specialized dashboards (e.g., Lab 07 has `cell-division-dashboard.html` and `mitosis-dashboard.html`).

---

## Dashboard Inventory

| Dashboard | Lab | Size | Key Features |
|-----------|-----|------|-------------|
| `lab-01_measurement-methods-dashboard.html` | Measurement | — | Unit converters, precision tools |
| `lab-02_probability-statistics-dashboard.html` | Probability | — | Dice simulators, distributions |
| `lab-03_microscopy-dashboard.html` | Microscopy | — | Virtual microscope, magnification |
| `lab-04_diffusion-membranes-dashboard.html` | Diffusion | — | Osmosis simulator, density mixing |
| `lab-05_ph-solutions-dashboard.html` | pH & Solutions | — | pH scale, buffer simulator |
| `lab-06_central-dogma-dashboard.html` | Central Dogma | — | Transcription/translation |
| `lab-07_cell-division-dashboard.html` | Cell Division | 26KB | Phase viewer, comparison table |
| `lab-07_mitosis-dashboard.html` | Cell Division | 92KB | Phase animator, virtual microscope, wound healing |
| `lab-08_inheritance-dashboard.html` | Inheritance | — | Punnett squares, pedigree |
| `lab-08_meiosis-dashboard.html` | Inheritance | — | Meiosis animations |
| `lab-09_enzymes-dashboard.html` | Enzymes | 107KB | Reaction rates, enzyme kinetics |
| `lab-10_tissues-dashboard.html` | Tissues | — | Tissue identification |
| `lab-11_skeletal-system-dashboard.html` | Skeletal | — | Bone anatomy |
| `lab-12_muscular-system-dashboard.html` | Muscular | — | Muscle contraction |
| `lab-13_nervous-system-dashboard.html` | Nervous | — | Neuron signaling, reaction time |
| `lab-14_microbiology-dashboard.html` | Microbiology | — | Gram stain, microbe comparison |
| `lab-15_cardiopulmonary-dashboard.html` | Cardiopulmonary | — | Heart, vessels, gas exchange |
| `lab-16_exam-03-review-dashboard.html` | Exam 03 review | — | Modules 11–15 checklist |

---

## Architecture Pattern

All dashboards follow a consistent sidebar + main content layout:

```
┌───────────────┬─────────────────────────────────────────────┐
│   SIDEBAR     │                MAIN CONTENT                 │
│               │                                             │
│  BIOL-8       │  ┌─ Hero Banner ───────────────────────┐    │
│  Lab X        │  │  Title, description, topic tags      │    │
│               │  └─────────────────────────────────────┘    │
│  • Overview   │                                             │
│  1 Section    │  ┌─ Section 1 ─────────────────────────┐    │
│  2 Section    │  │  ┌── Card ──────────────────────┐   │    │
│  3 Section    │  │  │  Canvas + Controls + Stats   │   │    │
│  4 Section    │  │  └─────────────────────────────┘   │    │
│  5 Section    │  └─────────────────────────────────────┘    │
│               │                                             │
│  © 2026       │  ┌─ Section 2 ─────────────────────────┐    │
│               │  │  ...                                 │    │
└───────────────┴─────────────────────────────────────────────┘
```

---

## HTML Template

### Minimal Boilerplate

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lab X Dashboard: Topic | BIOL-8</title>
<style>
/* CSS Design System (see below) */
</style>
</head>
<body>
<div class="layout">
  <aside class="sidebar">
    <!-- Sidebar navigation -->
  </aside>
  <div class="main">
    <!-- Hero + Sections -->
  </div>
</div>
<script>
/* JavaScript Engine */
</script>
</body>
</html>
```

All CSS and JavaScript are **inline** — dashboards are single self-contained HTML files with zero external dependencies.

---

## CSS Design System

### CSS Variables

Every dashboard uses a standard set of CSS custom properties:

```css
:root {
  --bg: #f0f2f5;
  --card: #ffffff;
  --sidebar: #1a1a2e;
  --sidebar-hover: #252545;
  --accent: #c41e3a;         /* Primary red */
  --accent-light: #e8354f;
  --blue: #2563eb;
  --blue-light: #3b82f6;
  --green: #16a34a;
  --amber: #d97706;
  --purple: #7c3aed;
  --text: #1a1a1a;
  --text-muted: #6b7280;
  --border: #e5e7eb;
  --radius: 10px;
  --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
  --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
  --mono: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
}
```

### Core CSS Components

| Component | Class | Purpose |
|-----------|-------|---------|
| **Layout** | `.layout`, `.sidebar`, `.main` | Flexbox sidebar + main content |
| **Sidebar** | `.sidebar-header`, `.sidebar-nav`, `.sidebar-footer` | Fixed left nav |
| **Sections** | `.section`, `.section-header`, `.section-num`, `.section-title` | Numbered content sections |
| **Cards** | `.card`, `.card-title`, `.card-row`, `.card-row-3` | White content containers |
| **Buttons** | `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-outline`, `.btn-sm` | Interactive controls |
| **Stat Boxes** | `.stat-grid`, `.stat-box`, `.stat-val`, `.stat-label` | Numeric displays |
| **Badges** | `.badge`, `.badge-red`, `.badge-blue`, `.badge-green` | Status indicators |
| **Charts** | `.chart-wrap`, `canvas` | Canvas container |
| **Sliders** | `.slider-group`, `.slider-val` | Range input controls |
| **Toggle Groups** | `.toggle-group`, `.toggle-btn`, `.phase-btn` | Button groups |
| **Analysis** | `.analysis-result`, `.ar-title`, `.ar-pass`, `.ar-fail` | Result panels |
| **Hero** | `.hero`, `.bio-tags`, `.bio-tag` | Top banner |

### Responsive Breakpoints

```css
@media (max-width: 900px) {
  .card-row, .card-row-3 { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .sidebar { display: none; }
  .main { margin-left: 0; padding: 16px; }
}
```

---

## Sidebar Navigation

```html
<aside class="sidebar">
  <div class="sidebar-header">
    <h1>BIOL-8: Human Biology</h1>
    <p>Lab X &mdash; Topic Name</p>
  </div>
  <nav class="sidebar-nav">
    <a href="#hero" class="active">
      <span class="nav-num">&bull;</span> Overview
    </a>
    <a href="#part1"><span class="nav-num">1</span> Section Name</a>
    <a href="#part2"><span class="nav-num">2</span> Section Name</a>
  </nav>
  <div class="sidebar-footer">
    Interactive Lab Dashboard<br>&copy; 2026 BIOL-8
  </div>
</aside>
```

### Scroll Spy

Active nav highlighting on scroll:

```javascript
const navLinks = document.querySelectorAll('.sidebar-nav a');
window.addEventListener('scroll', () => {
  let current = '';
  document.querySelectorAll('.section, .hero').forEach(s => {
    if (window.scrollY >= s.offsetTop - 100) current = s.id;
  });
  navLinks.forEach(a => {
    a.classList.remove('active');
    if (a.getAttribute('href') === '#' + current) a.classList.add('active');
  });
});
```

---

## Section Structure

Each numbered section follows this pattern:

```html
<div class="section" id="part1">
  <div class="section-header">
    <div class="section-num">1</div>
    <div>
      <div class="section-title">Section Title</div>
      <div class="section-subtitle">Brief description</div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">Card Title</div>
    <div class="chart-wrap"><canvas id="my-canvas" height="350"></canvas></div>
    <div class="btn-group">
      <button class="btn btn-primary" onclick="runAction()">Action</button>
      <button class="btn btn-outline" onclick="resetAction()">Reset</button>
    </div>
    <div class="stat-grid">
      <div class="stat-box stat-accent">
        <div class="stat-val" id="stat-1">0</div>
        <div class="stat-label">Label</div>
      </div>
    </div>
  </div>
</div>
```

---

## JavaScript Patterns

### Utility Functions

```javascript
const $ = id => document.getElementById(id);
const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const lerp = (a, b, t) => a + (b - a) * t;
```

### Canvas Setup

High-DPI canvas initialization:

```javascript
function getCtx(id) {
  const c = $(id);
  const dpr = window.devicePixelRatio || 1;
  const w = c.offsetWidth || c.width || 300;
  const h = c.offsetHeight || c.height || 150;
  c.width = w * dpr;
  c.height = h * dpr;
  const ctx = c.getContext('2d');
  ctx.scale(dpr, dpr);
  ctx.W = w;
  ctx.H = h;
  return ctx;
}
```

### Bar Chart Helper

```javascript
function drawBarChart(ctx, opts = {}) {
  const { labels, values, colors, maxVal } = opts;
  // ... standard bar chart with rounded tops, grid lines, labels
}
```

### Line Chart Helper

```javascript
function drawLineChart(ctx, series, opts = {}) {
  // series: [{data: [], color: '#c41e3a', dots: true}]
  // opts: {yMin, yMax, refLine, xLabel}
}
```

### Animation Loop

For phase animators and simulations:

```javascript
let animId = null;

function animate() {
  const speed = parseInt($('speed-slider').value);
  // Update state
  // Redraw canvas
  animId = requestAnimationFrame(animate);
}

function togglePlay() {
  if (animId) {
    cancelAnimationFrame(animId);
    animId = null;
    $('play-btn').textContent = 'Play';
  } else {
    $('play-btn').textContent = 'Pause';
    animate();
  }
}
```

---

## Common Interactive Components

### Phase Animator

Step through biological phases with play/pause controls and descriptive panels.

**Structure**: Canvas visualization + navigation buttons + speed slider + stat grid + description panel.

**State**: Phase index, animation timer, transition progress.

### Virtual Microscope

Clickable field-of-view where students classify cells by phase.

**Structure**: Canvas with clickable cells + phase classification buttons + accuracy tracking.

### Simulation

Run/reset simulations with parameter controls and live charts.

**Structure**: Parameter sliders + run/reset buttons + output chart canvas + result stat boxes.

### Knowledge Check Quiz

Multiple-choice or identification questions with immediate feedback.

**Structure**: Question text + answer buttons + feedback panel + score tracking.

---

## Design Guidelines

| Guideline | Rule |
|-----------|------|
| **Color** | Use CSS variables, never hardcoded hex in JS (except canvas drawing) |
| **Typography** | Use `var(--font)` for text, `var(--mono)` for numbers |
| **Spacing** | Cards have `padding: 24px`, sections have `margin-bottom: 40px` |
| **Stat values** | Large bold monospace numbers (28px+) |
| **Animations** | Use `requestAnimationFrame`, provide speed controls |
| **Responsiveness** | Mobile hides sidebar, single-column cards |
| **Accessibility** | Canvas content should have text descriptions in stat boxes |
| **Self-contained** | Zero external dependencies — no CDN, no imports |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [LAB_FORMAT.md](LAB_FORMAT.md) | Lab protocol authoring guide |
| [OUTPUT_HTML.md](OUTPUT_HTML.md) | HTML output format details |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [ORCHESTRATION.md](ORCHESTRATION.md) | Generation workflows |
