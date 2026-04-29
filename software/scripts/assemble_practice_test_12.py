#!/usr/bin/env python3
"""Build practice-test-12 Part A from PT01–PT11 slices + ecology/evolution MC; cycle correct letters."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PT_DIR = ROOT / "course_development" / "biol-8" / "course" / "practice_tests"
STUDENT_OUT = PT_DIR / "practice-test-12.md"
KEY_OUT = PT_DIR / "practice-test-12_key.md"
PART_BC = PT_DIR / "pt12_part_bc_fragment.md"

# Five questions per module × 17 modules = 85.
# (source_md, local_q_nums, key_md, key_kind) — key_kind: "table" (PT01) or "lines"
SPEC: list[tuple[str, list[int], str, str]] = [
    ("practice-test-01.md", [1, 2, 3, 4, 5], "practice-test-01_key.md", "table"),
    ("practice-test-01.md", [9, 10, 11, 12, 13], "practice-test-01_key.md", "table"),
    ("practice-test-01.md", [17, 18, 19, 20, 21], "practice-test-01_key.md", "table"),
    ("practice-test-01.md", [25, 26, 27, 28, 29], "practice-test-01_key.md", "table"),
    ("practice-test-02.md", [1, 2, 3, 4, 5], "practice-test-02_key.md", "manual_pt02"),
    ("practice-test-02.md", [9, 10, 11, 12, 13], "practice-test-02_key.md", "manual_pt02"),
    ("practice-test-03.md", [1, 2, 3, 4, 5], "practice-test-03_key.md", "lines"),
    ("practice-test-04.md", [1, 2, 3, 4, 5], "practice-test-04_key.md", "lines"),
    ("practice-test-05.md", [1, 2, 3, 4, 5], "practice-test-05_key.md", "lines"),
    ("practice-test-06.md", [1, 2, 3, 4, 5], "practice-test-06_key.md", "lines"),
    ("practice-test-07.md", [1, 2, 3, 4, 5], "practice-test-07_key.md", "lines"),
    ("practice-test-08.md", [1, 2, 3, 4, 5], "practice-test-08_key.md", "lines"),
    ("practice-test-09.md", [1, 2, 3, 4, 5], "practice-test-09_key.md", "lines"),
    ("practice-test-10.md", [1, 2, 3, 4, 5], "practice-test-10_key.md", "lines"),
    ("practice-test-11.md", [1, 2, 3, 4, 5], "practice-test-11_key.md", "lines"),
]

MODULE_HEADINGS = [
    "### Module 01: Exploring Life Science",
    "### Module 02: Chemistry of Life",
    "### Module 03: Biomolecules",
    "### Module 04: Cellular Function",
    "### Module 05: Membranes",
    "### Module 06: Metabolism",
    "### Module 07: Genetics",
    "### Module 08: Cell Division",
    "### Module 09: Tissues and the Animal Body",
    "### Module 10: Inheritance",
    "### Module 11: Skeletal System",
    "### Module 12: Muscular System",
    "### Module 13: Nervous System",
    "### Module 14: Microbiology",
    "### Module 15: Cardiopulmonary System",
    "### Module 16: Ecology",
    "### Module 17: Evolution",
]

# Built-in MC for modules 16–17 (correct letter before cycling = as authored)
BUILTIN: list[tuple[str, str, list[tuple[str, str]], str]] = [
    # stem, correct_letter, [(A,text),(B,text)...], rationale one-liner
    (
        "In most ecosystems, energy enters primarily as sunlight and is converted by:",
        "B",
        [
            ("A", "Herbivores fixing carbon from bone minerals"),
            ("B", "Producers such as plants and algae"),
            ("C", "Decomposers creating energy from heat alone"),
            ("D", "Consumers synthesizing glucose without chlorophyll"),
        ],
        "Producers capture light energy and build organic molecules that feed other trophic levels.",
    ),
    (
        "A food chain links producers to successive:",
        "C",
        [
            ("A", "abiotic reservoirs only"),
            ("B", "photosynthetic pigments"),
            ("C", "consumer trophic levels"),
            ("D", "blood types"),
        ],
        "Energy and biomass typically pass producer → primary consumer → higher consumers.",
    ),
    (
        "Which pair best contrasts biotic versus abiotic factors?",
        "A",
        [
            ("A", "Trees versus rainfall"),
            ("B", "Wind versus sunlight"),
            ("C", "Temperature versus pH"),
            ("D", "Soil minerals versus altitude"),
        ],
        "Biotic factors are living; abiotic factors are non-living chemical/physical conditions.",
    ),
    (
        "Compared with energy, nutrients such as nitrogen often:",
        "D",
        [
            ("A", "leave ecosystems permanently after one pass"),
            ("B", "flow in one direction only without recycling"),
            ("C", "increase in quantity at each trophic transfer"),
            ("D", "cycle among organisms and the environment"),
        ],
        "Materials recycle through biogeochemical cycles; energy dissipates as heat.",
    ),
    (
        "Logistic population growth levels off mainly because environments have finite:",
        "C",
        [
            ("A", "mutation rates"),
            ("B", "oxygen only"),
            ("C", "resources (carrying capacity)"),
            ("D", "chromosome counts"),
        ],
        "Carrying capacity (K) reflects limiting resources and space.",
    ),
    (
        "Natural selection acts primarily on:",
        "B",
        [
            ("A", "traits acquired during an individual adult lifetime"),
            ("B", "heritable variation affecting reproduction and survival"),
            ("C", "random environmental noise unrelated to genes"),
            ("D", "goals or intentions of organisms"),
        ],
        "Selection requires variation, inheritance, and differences in survival/reproduction.",
    ),
    (
        "Which statement best distinguishes homology from analogy?",
        "A",
        [
            ("A", "Homology reflects shared ancestry; analogy reflects similar function by different ancestry"),
            ("B", "Homology always means identical DNA sequences"),
            ("C", "Analogous structures never look alike"),
            ("D", "Homology applies only to bacteria"),
        ],
        "Homologous traits descend from a common ancestor; analogous traits converge by similar roles.",
    ),
    (
        "Genetic drift has the strongest effects when populations are:",
        "C",
        [
            ("A", "infinitely large"),
            ("B", "heterozygous at every locus"),
            ("C", "small"),
            ("D", "free of mutation"),
        ],
        "Chance allele-frequency shifts matter most when sampling error is large (small N).",
    ),
    (
        "Reproductive isolation tends to increase when:",
        "D",
        [
            ("A", "gene flow is unlimited between groups"),
            ("B", "two populations share identical mates every generation"),
            ("C", "hybrids always have higher fitness than parents"),
            ("D", "barriers reduce successful mating or viable/fertile offspring"),
        ],
        "Barriers to gene flow allow divergence—prezygotic or postzygotic mechanisms.",
    ),
    (
        "Which fossil observation most directly supports common ancestry of vertebrates?",
        "B",
        [
            ("A", "Identical resting heart rates across all species"),
            ("B", "Sequential limb/bone patterns consistent with modification from shared forms"),
            ("C", "Species living at identical latitudes"),
            ("D", "Same number of offspring per clutch"),
        ],
        "Transitional similarities in anatomy align with descent with modification.",
    ),
]


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_key_table_pt01(text: str) -> dict[int, tuple[str, str]]:
    """Map Q -> (letter, explanation tail)."""
    out: dict[int, tuple[str, str]] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if "Q" in line and "Answer" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 3:
            continue
        try:
            q = int(parts[0])
        except ValueError:
            continue
        letter = parts[1].strip().upper()
        if letter not in "ABCD":
            continue
        expl = parts[2]
        out[q] = (letter, expl)
    return out


def parse_key_lines(text: str) -> dict[int, tuple[str, str]]:
    """Lines like: 12. **C** — explanation."""
    out: dict[int, tuple[str, str]] = {}
    pat = re.compile(r"^(\d+)\.\s+\*\*([ABCD])\*\*\s+[—\-]\s+(.*)$")
    for line in text.splitlines():
        m = pat.match(line.strip())
        if not m:
            continue
        q = int(m.group(1))
        letter = m.group(2)
        expl = m.group(3).strip()
        out[q] = (letter, expl)
    return out


# PT02 table key is misaligned with current practice-test-02.md numbering after Q4 — fixed rationales.
PT02_MANUAL: dict[int, tuple[str, str]] = {
    1: (
        "B",
        'Integral membrane proteins move laterally in the lipid bilayer—the "fluid mosaic."',
    ),
    2: ("C", "Hydrophobic tails cluster inward, away from aqueous environments."),
    3: ("B", "Cholesterol buffers membrane fluidity across temperature changes."),
    4: ("B", "Integral (transmembrane) proteins span from one surface to the other."),
    5: (
        "C",
        "Hypotonic surroundings cause net water influx—red blood cells swell and may lyse.",
    ),
    6: ("B", "Simple diffusion moves substances down their gradient without ATP."),
    7: ("C", "The Na⁺/K⁺ pump moves ions against gradients using ATP (active transport)."),
    8: ('B', 'Phagocytosis is "cell eating"—large particles engulfed by vesicles.'),
    9: ("B", "Metabolism includes all chemical reactions (anabolism + catabolism)."),
    10: ("B", "Exergonic reactions release energy when bonds are rearranged."),
    11: ("B", "Enzymes speed reactions by lowering activation energy."),
    12: ("B", "The substrate binds at the enzyme active site."),
    13: ("A", "Energy cannot be created or destroyed—only transformed/moved."),
}


def get_key_map(key_file: str, kind: str) -> dict[int, tuple[str, str]]:
    if kind == "manual_pt02":
        return PT02_MANUAL
    text = load(PT_DIR / key_file)
    if kind == "table":
        return parse_key_table_pt01(text)
    return parse_key_lines(text)


def mc_section_only(md: str) -> str:
    """Everything from first '## Part A' through before '## Part B' or end."""
    m = re.search(r"## Part A:.*?(?=## Part B:|## Part C:|$)", md, re.DOTALL | re.IGNORECASE)
    if not m:
        return md
    return m.group(0)


def split_question_blocks(section: str) -> dict[int, str]:
    """Split MC section into blocks keyed by question number."""
    blocks: dict[int, str] = {}
    parts = re.split(r"(?=^\*\*\d+\.\*\*)", section, flags=re.MULTILINE)
    for p in parts:
        m = re.match(r"^\*\*(\d+)\.\*\*", p.strip(), re.MULTILINE)
        if not m:
            continue
        blocks[int(m.group(1))] = p.strip()
    return blocks


def parse_options(block: str) -> tuple[str, list[tuple[str, str]]]:
    """Return stem text (markdown line after **N.**) and list (A-D, text)."""
    lines = block.strip().splitlines()
    if not lines:
        return "", []
    first = lines[0]
    mnum = re.match(r"^\*\*\d+\.\*\*\s*(.*)$", first.strip())
    stem_first = mnum.group(1).strip() if mnum else ""
    stem_lines = [stem_first] if stem_first else []
    opts: list[tuple[str, str]] = []
    i = 1
    while i < len(lines):
        line = lines[i].rstrip()
        om = re.match(r"^([ABCD])\)\s*(.*)$", line.strip())
        if om:
            letter = om.group(1)
            rest = om.group(2).strip()
            opts.append((letter, rest))
            i += 1
            continue
        if opts:
            break
        stem_lines.append(line.strip())
        i += 1
    stem = " ".join(x for x in stem_lines if x).strip()
    while i < len(lines):
        om = re.match(r"^([ABCD])\)\s*(.*)$", lines[i].strip())
        if om:
            opts.append((om.group(1), om.group(2).strip()))
        i += 1
    return stem, opts


def reorder_options(
    opts: list[tuple[str, str]], correct_letter: str, target_letter: str
) -> list[tuple[str, str]]:
    letters = "ABCD"
    texts = [t for _, t in opts[:4]]
    if len(texts) != 4:
        raise ValueError(f"Need 4 options, got {len(texts)}")
    ci = letters.index(correct_letter.upper())
    ti = letters.index(target_letter.upper())
    new_contents = [""] * 4
    for j in range(4):
        new_contents[j] = texts[(ci + (j - ti)) % 4]
    return [(letters[k], new_contents[k]) for k in range(4)]


def format_question(global_num: int, stem: str, opts: list[tuple[str, str]]) -> str:
    lines = [f"**{global_num}.** {stem}", ""]
    for letter, text in opts:
        lines.append(f"{letter}) {text}")
    return "\n".join(lines)


def cycle_letter(global_q: int) -> str:
    return "ABCD"[(global_q - 1) % 4]


def main() -> None:
    student_chunks: list[str] = []
    key_lines: list[str] = []

    hdr = """# BIOL-8 Practice Test 12

## Comprehensive Final Exam Preparation (Modules 01–17)

**Instructions:** This practice test samples five multiple-choice items per module (Modules **01–17**) plus written items aligned with each module. Answer to the best of your ability.

---

## Part A: Multiple Choice (85 questions)

*Choose the best answer. Items **1–85** follow module order (**01** through **17**); **Module 01** begins item **1**.*

"""

    student_chunks.append(hdr)

    key_hdr = """# Practice Test 12 — Answer Key

## Comprehensive Final Exam Preparation (Modules 01–17)

---

## Part A: Multiple Choice

"""

    global_q = 1

    for (src, locals_, keyf, kind), heading in zip(SPEC, MODULE_HEADINGS[:15]):
        md = load(PT_DIR / src)
        sec = mc_section_only(md)
        blocks_map = split_question_blocks(sec)
        keys = get_key_map(keyf, kind)

        student_chunks.append(f"{heading}\n")
        for ln in locals_:
            blk = blocks_map.get(ln)
            if blk is None:
                raise SystemExit(f"Missing Q{ln} in {src}")
            stem, opts = parse_options(blk)
            if len(opts) != 4:
                raise SystemExit(f"Bad option count in {src} Q{ln}: {opts!r}")
            kl = keys.get(ln)
            if not kl:
                raise SystemExit(f"Missing key for {src} Q{ln}")
            correct_letter, rationale = kl
            tgt = cycle_letter(global_q)
            new_opts = reorder_options(opts, correct_letter, tgt)
            student_chunks.append(format_question(global_q, stem, new_opts))
            student_chunks.append("")
            key_lines.append(f"{global_q}. **{tgt}** — {rationale}")
            global_q += 1

    # Builtin ecology + evolution (modules 16–17)
    for mod_idx, heading in enumerate(MODULE_HEADINGS[15:17], start=16):
        student_chunks.append(f"{heading}\n")
        chunk = BUILTIN[(mod_idx - 16) * 5 : (mod_idx - 16) * 5 + 5]
        for stem, correct_letter, pairs, rationale in chunk:
            tgt = cycle_letter(global_q)
            new_opts = reorder_options(list(pairs), correct_letter, tgt)
            student_chunks.append(format_question(global_q, stem, new_opts))
            student_chunks.append("")
            key_lines.append(f"{global_q}. **{tgt}** — {rationale}")
            global_q += 1

    if global_q != 86:
        raise SystemExit(f"Expected 85 MC items, got {global_q - 1}")

    key_body = "\n\n".join(key_lines) + "\n\n---\n"

    part_bc = load(PART_BC)
    if "## Part B" not in part_bc:
        raise SystemExit("Fragment missing Part B")

    student_doc = "\n".join(student_chunks).rstrip() + "\n\n---\n\n" + part_bc.strip() + "\n"

    # Append existing Part B/C key from current key file if present (preserve rubrics)
    old_key = load(KEY_OUT) if KEY_OUT.exists() else ""
    m_old = re.search(r"(## Part B:.*)$", old_key, re.DOTALL | re.IGNORECASE)
    if m_old:
        full_key = key_hdr + key_body + m_old.group(1).strip() + "\n"
    else:
        full_key = key_hdr + key_body + "\n*(Missing Part B/C key — regenerate)*\n"

    STUDENT_OUT.write_text(student_doc, encoding="utf-8")
    KEY_OUT.write_text(full_key, encoding="utf-8")
    print(f"Wrote {STUDENT_OUT}")
    print(f"Wrote {KEY_OUT}")


if __name__ == "__main__":
    main()
