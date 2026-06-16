#!/usr/bin/env python3
"""Generate aligned BIOL-1 lab dashboard HTML files.

The dashboard files are source materials copied into ``PUBLISHED/``.  This
generator keeps their filenames, titles, and study prompts aligned with the
active lab markdown files.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_DIR = (
    REPO_ROOT / "course_development" / "biol-1" / "course" / "labs" / "dashboards"
)


@dataclass(frozen=True)
class LabDashboardSpec:
    number: int
    slug: str
    title: str
    module: str
    focus: str
    evidence: tuple[str, str, str]
    checkpoints: tuple[str, str, str]
    terms: tuple[str, str, str, str]

    @property
    def filename(self) -> str:
        return f"lab-{self.number:02d}_{self.slug}-dashboard.html"


SPECS: tuple[LabDashboardSpec, ...] = (
    LabDashboardSpec(
        1,
        "measurement-methods",
        "Introduction to Scientific Measurement",
        "Module 01",
        "Practice accurate observation, units, and repeated measurements.",
        ("Observation", "Measurement", "Repeatability"),
        ("Record units every time.", "Use repeated trials.", "Separate data from interpretation."),
        ("variable", "unit", "trial", "average"),
    ),
    LabDashboardSpec(
        2,
        "probability-statistics",
        "Probability and Statistics",
        "Module 02",
        "Use chance models and summary statistics to reason from data.",
        ("Counts", "Expected ratio", "Observed ratio"),
        ("Compare expected and observed outcomes.", "Look for sample-size effects.", "Explain variation without overclaiming."),
        ("probability", "sample size", "ratio", "variation"),
    ),
    LabDashboardSpec(
        3,
        "microscopy",
        "Introduction to Light Microscopy",
        "Module 03",
        "Build careful microscope habits and connect magnification to evidence.",
        ("Magnification", "Field of view", "Cell structures"),
        ("Start on low power.", "Center before increasing magnification.", "Draw only what is observed."),
        ("lens", "focus", "field of view", "resolution"),
    ),
    LabDashboardSpec(
        4,
        "liquid-chemistry",
        "Liquid Chemistry",
        "Module 05",
        "Connect diffusion, viscosity, redox change, and dilution to cell chemistry.",
        ("Diffusion rate", "Color change", "Dilution gradient"),
        ("Compare water and methyl cellulose.", "Count drops before color loss.", "Explain molecules in diluted solutions."),
        ("diffusion", "viscosity", "redox", "dilution"),
    ),
    LabDashboardSpec(
        5,
        "viewing-life",
        "Viewing Life",
        "Module 06",
        "Use direct observation to connect structure and function in living systems.",
        ("Specimen", "Structure", "Function"),
        ("Describe the structure first.", "Infer function from evidence.", "Note uncertainty explicitly."),
        ("cell", "tissue", "structure", "function"),
    ),
    LabDashboardSpec(
        6,
        "exam-review",
        "Exam 01 Review",
        "Review: Modules 01-06",
        "Organize the first unit around evidence, chemistry, cells, membranes, and metabolism.",
        ("Strong topics", "Needs review", "Practice plan"),
        ("Use the module list as a checklist.", "Explain concepts without notes.", "Prioritize missed practice items."),
        ("science", "chemistry", "cell", "metabolism"),
    ),
    LabDashboardSpec(
        7,
        "molecular-genetics",
        "Molecular Genetics",
        "Module 07",
        "Trace information flow from DNA to RNA to protein.",
        ("DNA sequence", "RNA message", "Protein product"),
        ("Keep base-pairing rules straight.", "Separate transcription from translation.", "Connect mutations to protein changes."),
        ("DNA", "RNA", "codon", "mutation"),
    ),
    LabDashboardSpec(
        8,
        "cellular-genetics",
        "Cellular Genetics",
        "Module 08",
        "Compare mitosis and meiosis as chromosome-movement processes.",
        ("Starting cell", "Division steps", "Ending cells"),
        ("Identify what separates in each division.", "Track chromosome number.", "Connect meiosis to variation."),
        ("mitosis", "meiosis", "chromosome", "gamete"),
    ),
    LabDashboardSpec(
        9,
        "inheritance-genetics",
        "Inheritance Genetics",
        "Module 09",
        "Use allele models to predict and explain inheritance patterns.",
        ("Parent genotypes", "Gametes", "Offspring ratios"),
        ("Define symbols before solving.", "Show the Punnett square.", "Distinguish genotype from phenotype."),
        ("allele", "genotype", "phenotype", "Punnett square"),
    ),
    LabDashboardSpec(
        10,
        "epigenetics",
        "Epigenetics",
        "Module 10",
        "Explain how gene activity can change without changing the DNA sequence.",
        ("Signal", "Gene activity", "Trait effect"),
        ("Separate DNA sequence from gene expression.", "Use environment carefully.", "Avoid claiming acquired traits rewrite genes."),
        ("methylation", "histone", "expression", "environment"),
    ),
    LabDashboardSpec(
        11,
        "genomics-biotechnology",
        "Genomics and Biotechnology",
        "Module 11",
        "Connect DNA tools to evidence, diagnosis, and biotechnology decisions.",
        ("DNA sample", "Tool used", "Interpretation"),
        ("State what the tool detects.", "Separate evidence from decision.", "Name benefits and risks."),
        ("PCR", "gel", "CRISPR", "genome"),
    ),
    LabDashboardSpec(
        12,
        "exam-02-review",
        "Exam 02 Review",
        "Review: Modules 07-11",
        "Integrate molecular genetics, cell division, inheritance, epigenetics, and biotechnology.",
        ("Confident concept", "Confusing concept", "Next practice"),
        ("Build a one-page concept map.", "Explain DNA-to-trait links.", "Practice genetics problems slowly."),
        ("gene", "chromosome", "inheritance", "biotechnology"),
    ),
    LabDashboardSpec(
        13,
        "darwin-evolution",
        "Darwin and Evolution",
        "Module 12",
        "Use variation, selection, and reproductive success to explain adaptation.",
        ("Variation", "Selection pressure", "Outcome"),
        ("Define fitness as reproduction.", "Focus on populations.", "Avoid saying individuals evolve."),
        ("fitness", "adaptation", "selection", "population"),
    ),
    LabDashboardSpec(
        14,
        "how-populations-evolve",
        "How Populations Evolve",
        "Module 13",
        "Compare evolutionary mechanisms that change allele frequencies.",
        ("Mechanism", "Population size", "Allele change"),
        ("Separate drift from selection.", "Use migration for gene flow.", "Use Hardy-Weinberg as a baseline."),
        ("allele frequency", "drift", "gene flow", "Hardy-Weinberg"),
    ),
    LabDashboardSpec(
        15,
        "macroevolution",
        "Macroevolution",
        "Module 14",
        "Connect speciation, evidence, and phylogenies across deep time.",
        ("Barrier", "Divergence", "Evidence"),
        ("Name the species concept used.", "Connect trees to common ancestry.", "Use fossils as historical evidence."),
        ("species", "speciation", "phylogeny", "fossil"),
    ),
    LabDashboardSpec(
        16,
        "population-systems-ecology",
        "Population and Systems Ecology",
        "Module 15",
        "Track populations, interactions, and ecosystem feedbacks.",
        ("Population", "Interaction", "System effect"),
        ("Identify the level of organization.", "Connect cause and feedback.", "Use graphs to describe change over time."),
        ("population", "community", "ecosystem", "feedback"),
    ),
    LabDashboardSpec(
        17,
        "exam-03-review",
        "Exam 03 Review",
        "Review: Modules 12-15",
        "Prepare for the evolution and ecology unit exam with evidence-based review.",
        ("Evolution concept", "Ecology concept", "Practice target"),
        ("Use the four-module checklist.", "Explain mechanisms in plain language.", "Write one full free-response answer."),
        ("evolution", "selection", "speciation", "ecology"),
    ),
)


def render_dashboard(spec: LabDashboardSpec) -> str:
    terms = "\n".join(f"<li>{escape(term)}</li>" for term in spec.terms)
    evidence_cells = "\n".join(
        f"<label><span>{escape(label)}</span><textarea rows=\"3\"></textarea></label>"
        for label in spec.evidence
    )
    checkpoint_items = "\n".join(
        f"<label><input type=\"checkbox\"> <span>{escape(item)}</span></label>"
        for item in spec.checkpoints
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lab {spec.number} Dashboard: {escape(spec.title)} | BIOL-1</title>
<style>
:root {{
  --bg: #f5f7fb;
  --ink: #18202f;
  --muted: #5f6b7a;
  --card: #ffffff;
  --line: #d9e1ec;
  --accent: #b42338;
  --blue: #1d4ed8;
  --green: #15803d;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  color: var(--ink);
  background: var(--bg);
  line-height: 1.55;
}}
header {{
  background: #152033;
  color: white;
  padding: 24px;
}}
header p {{ color: #c9d4e5; margin: 4px 0 0; }}
main {{ max-width: 980px; margin: 0 auto; padding: 24px; }}
.grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
.card {{
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}}
.label {{ color: var(--muted); font-size: 12px; font-weight: 700; text-transform: uppercase; }}
h1 {{ margin: 0; font-size: 28px; }}
h2 {{ margin: 0 0 10px; font-size: 20px; }}
ul {{ margin: 8px 0 0; padding-left: 20px; }}
label {{ display: block; font-weight: 700; margin: 10px 0; }}
label span {{ display: block; margin-bottom: 4px; }}
textarea {{
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 10px;
  min-height: 72px;
  font: inherit;
}}
input[type="checkbox"] {{ transform: translateY(1px); }}
button {{
  border: 0;
  border-radius: 8px;
  padding: 10px 14px;
  background: var(--blue);
  color: white;
  font-weight: 700;
  cursor: pointer;
}}
.pill {{
  display: inline-block;
  border-radius: 999px;
  padding: 4px 10px;
  background: #eaf1ff;
  color: var(--blue);
  font-size: 13px;
  font-weight: 700;
  margin: 3px 4px 3px 0;
}}
.status {{ color: var(--green); font-weight: 700; margin-left: 10px; }}
@media (max-width: 720px) {{ .grid {{ grid-template-columns: 1fr; }} main {{ padding: 14px; }} }}
</style>
</head>
<body>
<header>
  <div class="label">BIOL-1 General Biology</div>
  <h1>Lab {spec.number}: {escape(spec.title)}</h1>
  <p>{escape(spec.module)} companion dashboard</p>
</header>
<main>
  <section class="card">
    <h2>Focus</h2>
    <p>{escape(spec.focus)}</p>
    <div>
      {"".join(f'<span class="pill">{escape(term)}</span>' for term in spec.terms)}
    </div>
  </section>

  <section class="grid">
    <div class="card">
      <div class="label">Observe</div>
      <p>What do you see, count, measure, or compare?</p>
    </div>
    <div class="card">
      <div class="label">Explain</div>
      <p>What biological idea explains the evidence?</p>
    </div>
    <div class="card">
      <div class="label">Check</div>
      <p>What uncertainty or alternate explanation remains?</p>
    </div>
  </section>

  <section class="card">
    <h2>Evidence Capture</h2>
    {evidence_cells}
    <button type="button" id="save">Save Notes</button><span class="status" id="status"></span>
  </section>

  <section class="card">
    <h2>Concept Check</h2>
    {checkpoint_items}
  </section>

  <section class="card">
    <h2>Key Terms</h2>
    <ul>
      {terms}
    </ul>
  </section>
</main>
<script>
const key = "biol1-lab-{spec.number:02d}-dashboard";
const fields = Array.from(document.querySelectorAll("textarea"));
try {{
  const saved = JSON.parse(localStorage.getItem(key) || "[]");
  fields.forEach((field, index) => {{ field.value = saved[index] || ""; }});
}} catch (error) {{
  console.warn("Could not load saved dashboard notes", error);
}}
document.getElementById("save").addEventListener("click", () => {{
  localStorage.setItem(key, JSON.stringify(fields.map(field => field.value)));
  document.getElementById("status").textContent = "Saved in this browser";
}});
</script>
</body>
</html>
"""


def main() -> None:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in DASHBOARD_DIR.glob("lab-*-dashboard.html"):
        old_file.unlink()
    for spec in SPECS:
        output_path = DASHBOARD_DIR / spec.filename
        output_path.write_text(render_dashboard(spec), encoding="utf-8")
        print(output_path.relative_to(REPO_ROOT))


if __name__ == "__main__":
    main()
