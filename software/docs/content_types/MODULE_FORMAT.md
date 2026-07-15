# Module Format Guide

> **Navigation**: [← Content Types](../README.md) | [Exam Format](EXAM_FORMAT.md) | [Practice Test Format](PRACTICE_TEST_FORMAT.md) | [Slides Format](SLIDES_FORMAT.md) | [Lab Format](../LAB_FORMAT.md) | [Course Structure](../COURSE_STRUCTURE.md) | [Architecture](../ARCHITECTURE.md)

Complete guide for authoring course modules. Each module is a self-contained content unit driven by a `module.toml` source-of-truth file that generates study guides, practice quizzes, and SVG visualizations.

---

## Directory Structure

```
module-NN-topic-name/
├── README.md                # Student-facing module overview
├── AGENTS.md                # Technical doc for tooling
├── module.toml               # Canonical typed source (source of truth)
├── questions.md             # Generated learning questions
├── keys-to-success.md       # Generated module study guide
├── practice-quiz.md         # Generated practice quiz
├── resources/               # (optional) module-local assets
└── output/                  # Generated; do not edit by hand
    ├── study-guides/
    │   ├── module-NN-name-questions.{md,pdf,docx}
    │   ├── module-NN-name-keys-to-success.{md,pdf,docx}
    │   └── module-NN-name-practice-quiz.{md,pdf,docx}
    └── website/index.html
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| **Module folder** | `module-NN-topic-words/` (zero-padded `NN`, lowercase, hyphenated) | `module-01-study-of-life` |
| **Source file** | `module.toml` (always at module root) | — |
| **Generated outputs** | Prefixed with full module slug | `module-01-study-of-life-questions.pdf` |

> **Rule**: `keys-to-success.md` must put `## Learning Objectives` as the first level-2 section after the title.

---

## module.toml Schema

The `module.toml` file is the **canonical typed source** for each module. All generated files derive from it. Never edit generated `.md` files directly — edit `module.toml` and rerun generation.

### `[module]` Section

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `number` | integer | Yes | Zero-padded module number (1–16 for BIOL-1) |
| `slug` | string | Yes | Directory slug, e.g. `"module-01-study-of-life"` |
| `title` | string | Yes | Human-readable module title |
| `lab` | string | Yes | Companion lab filename, e.g. `"lab-01_measurement-methods.md"` |
| `topics` | array&lt;string&gt; | Yes | 5 topic headings for the module |
| `contents` | array&lt;string&gt; | Yes | 5 content summaries (one per topic) |
| `learning_objectives` | array&lt;string&gt; | Yes | 5 learning objectives (verb-first) |
| `study_tips` | array&lt;string&gt; | Yes | 4 study tips for the module |
| `learning_questions` | array&lt;string&gt; | Yes | 10 learning questions for `questions.md` |

### `[[terms]]` Array

Key vocabulary terms for the module. Typically 5–8 entries.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Term name |
| `definition` | string | Yes | Concise definition |

### `[[practice_quiz]]` Array

Multiple-choice practice quiz items for `practice-quiz.md`. Typically 4–5 entries.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | Yes | Question stem |
| `options` | array&lt;string&gt; | Yes | 4 answer options (A–D) |
| `answer` | string | Yes | Correct option letter (`"A"`, `"B"`, `"C"`, or `"D"`) |
| `explanation` | string | Yes | Why the correct answer is right |

### `[[generated_images]]` Array

SVG visualization definitions. The canonical spine requires exactly **three** entries: `concept-map`, `process-model`, and `retrieval-card`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | `"concept-map"`, `"process-model"`, or `"retrieval-card"` |
| `title` | string | Yes | SVG title (uses module title) |
| `kind` | string | Yes | Same as `id` |
| `output` | string | Yes | Output path relative to module root |
| `prompt` | string | Yes | Generation prompt description |

#### concept-map fields

| Field | Type | Description |
|-------|------|-------------|
| `central_claim` | string | Core claim at the center of the map |
| `clusters` | array&lt;string&gt; | Cluster labels (e.g. Claim, Mechanism, Evidence) |
| `nodes` | array | Node objects: `id`, `label`, `detail`, `cluster` |
| `edges` | array | Edge objects: `source`, `target`, `label` |

#### process-model fields

| Field | Type | Description |
|-------|------|-------------|
| `inputs` | array&lt;string&gt; | Reasoning inputs |
| `outputs` | array&lt;string&gt; | Learning objective outputs |
| `feedbacks` | array&lt;string&gt; | Feedback loops |
| `constraints` | array&lt;string&gt; | Reasoning constraints |
| `stages` | array | Stage objects: `label`, `detail`, `emphasis` |

#### retrieval-card fields

| Field | Type | Description |
|-------|------|-------------|
| `terms` | array&lt;string&gt; | Terms to retrieve |
| `lab_connection` | string | Connection to same-numbered lab |
| `prompts` | array | Prompt objects: `prompt`, `check` |

---

## Complete module.toml Example

```toml
[module]
number = 1
slug = "module-01-study-of-life"
title = "Biology - The Study of Life"
lab = "lab-01_measurement-methods.md"
topics = [
  "What counts as life",
  "Science as a way of testing",
  "Organization from cells to ecosystems",
  "Evidence, variables, and measurement",
  "How biological explanations improve",
]
contents = [
  "Life is recognized by shared properties: cells, energy use, response, reproduction, regulation, and evolution.",
  "Scientific claims are tested with observations, comparisons, variables, and repeatable reasoning.",
  "Biological systems are organized across scales from molecules to biosphere.",
  "Data become useful when measurements are tied to a clear question and source of error.",
  "Strong explanations connect evidence to a claim and stay open to revision.",
]
learning_objectives = [
  "Distinguish living systems from nonliving examples using multiple characteristics.",
  "Separate hypotheses, predictions, observations, and conclusions in a scientific test.",
  "Place biological examples at the correct scale of organization.",
  "Identify variables and evidence in a simple investigation.",
  "Revise a biological explanation when new evidence appears.",
]
study_tips = [
  "Start with the module's central claim before memorizing vocabulary.",
  "Use the same-numbered lab as the evidence check for the module.",
  "Explain one mechanism in words, then redraw it as a simple diagram.",
  "Answer retrieval questions without notes, then revise with the terms list.",
]
learning_questions = [
  "Which characteristics together make something count as alive?",
  "How is a hypothesis different from a prediction?",
  # ... (10 total)
]

[[terms]]
name = "Cell"
definition = "Basic unit of life bounded by a membrane."

[[terms]]
name = "Homeostasis"
definition = "Regulation that keeps internal conditions within a workable range."

[[practice_quiz]]
question = "A student sees frost crystals slowly \"grow\" on a cold window overnight. Why don't biologists count this as life?"
options = [
  "Growth by itself is not enough; life needs cells, metabolism, response, and reproduction together.",
  "Crystals are too small to be considered alive.",
  "Crystals are never found in the natural world.",
  "Only warm objects can ever be alive.",
]
answer = "A"
explanation = "No single trait defines life. Living things share a set of properties together."

[[generated_images]]
id = "concept-map"
title = "Module 01: Biology - The Study of Life Evidence Map"
kind = "concept-map"
output = "resources/generated/module-01-concept-map.svg"
prompt = "Deterministic BIOL-1 SVG showing how Module 01 connects claim, mechanism, lab evidence, vocabulary, application, and misconception revision."
central_claim = "Biology - The Study of Life explains life criteria with measurement-based scientific explanation."
clusters = ["Claim", "Mechanism", "Evidence", "Application", "Revision"]

[[generated_images.nodes]]
id = "core"
label = "What counts as life"
detail = "Life is recognized by shared properties: cells, energy use, response, reproduction, regulation, and evolution."
cluster = "Claim"

[[generated_images.edges]]
source = "core"
target = "mechanism"
label = "requires"

[[generated_images]]
id = "process-model"
title = "Module 01: Biology - The Study of Life Reasoning Sequence"
kind = "process-model"
output = "resources/generated/module-01-process-model.svg"
prompt = "Deterministic BIOL-1 SVG tracing the Module 01 reasoning sequence."
inputs = ["What counts as life", "Science as a way of testing"]
outputs = ["Distinguish living systems from nonliving examples."]
feedbacks = ["lab-01_measurement-methods.md evidence checks understanding."]
constraints = ["A single trait is not enough to classify life."]

[[generated_images.stages]]
label = "What counts as life"
detail = "Life is recognized by shared properties."
emphasis = "Step 1"

[[generated_images]]
id = "retrieval-card"
title = "Module 01: Biology - The Study of Life Retrieval and Lab Check"
kind = "retrieval-card"
output = "resources/generated/module-01-retrieval-card.svg"
prompt = "Deterministic BIOL-1 SVG pairing Module 01 retrieval prompts with answer checks."
terms = ["Cell", "Homeostasis", "Metabolism", "Hypothesis", "Variable"]
lab_connection = "lab-01_measurement-methods.md supplies evidence for measurement choices."

[[generated_images.prompts]]
prompt = "Which characteristics together make something count as alive?"
check = "Distinguish living systems from nonliving examples using multiple characteristics."
```

---

## Generated Files

### keys-to-success.md

The module study guide. Generated from `module.toml` fields:
- `learning_objectives` → `## Learning Objectives` (must be first H2 section)
- `contents` → topic summaries
- `study_tips` → `## Study Tips`
- `terms` → `## Key Terms`

### questions.md

Practice questions for the module. Generated from `learning_questions` array (typically 10 questions).

### practice-quiz.md

Multiple-choice quiz. Generated from `[[practice_quiz]]` entries (typically 4–5 items with A–D options, answer key, and explanations).

---

## SVG Generation

Three canonical SVGs are generated per module from the `[[generated_images]]` entries:

| SVG | Kind | Purpose |
|-----|------|---------|
| **concept-map** | `concept-map` | Node-and-edge graph connecting claim → mechanism → evidence → vocabulary → application → revision |
| **process-model** | `process-model` | Sequential flow diagram with inputs, stages, feedbacks, and outputs |
| **retrieval-card** | `retrieval-card` | Retrieval prompts paired with answer checks, key terms, and lab connection |

### SVG Output Location

```
module-NN-name/
└── resources/
    └── generated/
        ├── module-NN-concept-map.svg
        ├── module-NN-process-model.svg
        └── module-NN-retrieval-card.svg
```

> **Contract**: The three SVGs must use the visual title from `module.toml`, include concise teaching points, and explicitly name the module title and same-numbered lab. These are consumed by the slide deck generator (see [SLIDES_FORMAT.md](SLIDES_FORMAT.md)).

---

## Generation Commands

```bash
cd software

# Generate all BIOL-1 outputs (all modules)
uv run python scripts/generate_all_outputs.py --course biol-1

# Generate a specific module's outputs
uv run python scripts/generate_module_renderings.py --course biol-1 --module 12

# Build the per-module HTML site
uv run python scripts/generate_module_website.py --course biol-1 --module 12
```

The end-to-end pipeline (`python publish.py` at repo root) runs these steps for every module and pushes results to `PUBLISHED/biol-1/`.

---

## BIOL-1 Module Inventory (16 modules)

| # | Directory |
|---|-----------|
| 01 | `module-01-study-of-life` |
| 02 | `module-02-basic-chemistry` |
| 03 | `module-03-organic-molecules` |
| 04 | `module-04-cells` |
| 05 | `module-05-membranes` |
| 06 | `module-06-metabolism` |
| 07 | `module-07-molecular-genetics` |
| 08 | `module-08-cellular-genetics` |
| 09 | `module-09-inheritance-genetics` |
| 10 | `module-10-epigenetics` |
| 11 | `module-11-genomics-biotechnology` |
| 12 | `module-12-darwin-evolution` |
| 13 | `module-13-how-populations-evolve` |
| 14 | `module-14-macroevolution` |
| 15 | `module-15-population-systems-ecology` |
| 16 | `module-16-capstone-systems-synthesis` |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [README.md](../README.md) | Content types index |
| [SLIDES_FORMAT.md](SLIDES_FORMAT.md) | Slide deck generation from module.toml |
| [../COURSE_STRUCTURE.md](../COURSE_STRUCTURE.md) | Course directory layout |
| [../ORCHESTRATION.md](../ORCHESTRATION.md) | Generation and publish pipeline |
| [../../../course_development/biol-1/course/AGENTS.md](../../../course_development/biol-1/course/AGENTS.md) | Course-level source documentation |
