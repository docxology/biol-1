"""Configuration constants and compiled regex patterns for exam-tools MC shuffling."""

from __future__ import annotations

import re
from typing import Final

# Balanced multiset for 45 questions (12 A, 11 each B/C/D).
FINAL_MC_SEED: Final[int] = 20260203

# Legacy correct letters for Part A (recovered BIOL-1 final before any reshuffle).
CORRECT_LETTERS_LEGACY_LAYOUT: Final[dict[int, str]] = {
    1: "B",
    2: "C",
    3: "B",
    4: "B",
    5: "B",
    6: "B",
    7: "B",
    8: "B",
    9: "C",
    10: "C",
    11: "C",
    12: "C",
    13: "B",
    14: "B",
    15: "B",
    16: "B",
    17: "A",
    18: "A",
    19: "C",
    20: "B",
    21: "C",
    22: "B",
    23: "A",
    24: "B",
    25: "B",
    26: "C",
    27: "B",
    28: "B",
    29: "B",
    30: "B",
    31: "B",
    32: "B",
    33: "B",
    34: "A",
    35: "B",
    36: "B",
    37: "B",
    38: "B",
    39: "B",
    40: "A",
    41: "B",
    42: "B",
    43: "B",
    44: "B",
    45: "B",
}

LEGACY_CORRECT_TEXTS: Final[dict[int, str]] = {
    1: "Atom → Molecule → Cell → Tissue → Organ",
    2: "A testable prediction or explanation that can be supported or refuted with evidence",
    3: "Ability of an organism to maintain stable internal conditions amid external change",
    4: "Protons in its atoms (under neutral atoms, sets identity of element)",
    5: "Share electrons between nuclei",
    6: "Hydrogen bonding creates an open lattice in ice that is less dense than liquid water",
    7: "Condensation / dehydration synthesis",
    8: "Nucleic acids (DNA / RNA)",
    9: "Proteins (sometimes RNA catalysts) that speed specific reactions by lowering activation energy",
    10: "All living organisms are made of cells and cells come from pre-existing cells "
    "(modern framing includes revisions but retains core ideas)",
    11: "Mitochondrion",
    12: "Membrane-bound nucleus",
    13: "A lipid bilayer with embedded proteins that can move laterally",
    14: "Down the molecule\u2019s concentration gradient without direct metabolic energy for the crossing itself",
    15: "Diffusion of **water** across a selectively permeable membrane",
    16: "ATP hydrolysis and phosphate transfer can be coupled to drive cellular work; ATP is continually "
    "regenerated rather than serving as permanent storage",
    17: "Uses oxygen and breaks fuel molecules to capture usable energy (often linked to ATP production)",
    18: "Binds substrates and catalyzes conversion to products for that reaction",
    19: "Ribosomes synthesizing polypeptides using an mRNA code",
    20: "DNA polymerase adding complementary nucleotides",
    21: "Contains ribose (often single-stranded functional molecules such as mRNA, tRNA, rRNA)",
    22: "Haploid (n)",
    23: "Prophase I of meiosis",
    24: "Two genetically identical diploid daughter cells (barring mutation)",
    25: "Alleles",
    26: "**3 dominant-looking : 1 recessive-looking** among offspring (classic single-gene expectation)",
    27: "Heterozygotes show an intermediate phenotype between homozygotes",
    28: "Alter gene activity **without** necessarily changing the DNA sequence itself",
    29: "Reduces transcription / promotes a gene-off state compared with unmethylated promoter regions "
    "in many examples",
    30: "One X is largely condensed / silenced in each somatic cell for dosage compensation",
    31: "Amplify targeted DNA sequences from small samples",
    32: "The positive electrode; smaller fragments often travel farther in a given time",
    33: "Target specific DNA sequences for cutting / editing with guide RNA assistance",
    34: "Populations tend to produce **more offspring than can survive and reproduce**",
    35: "Shared ancestry with structural modification under different selective regimes",
    36: "Relative contribution of alleles to future generations through survival and reproduction",
    37: "Move alleles between populations through migration and mating—often homogenizing allele "
    "frequencies between connected groups over time (depending on rates)",
    38: "Population size is **small** so random sampling shifts allele frequencies strongly between "
    "generations",
    39: "A mathematical **null / baseline** against which observed allele-frequency change is interpreted",
    40: "Temporal isolation",
    41: "Postzygotic reduced hybrid fertility",
    42: "Allopatric speciation starting with geographic isolation",
    43: "Growth slows as **N** approaches **K** (carrying capacity)",
    44: "Density-dependent regulation (impact intensifies with density in many textbook examples)",
    45: "Lost largely as heat between trophic transfers—supporting fewer top consumers than low trophic "
    "levels per unit primary production",
}

# Regex patterns for parsing exam markdown.
OPTION_LINE: Final[re.Pattern[str]] = re.compile(r"^(\s*)-\s([A-D])\)\s(.*)$")
QUESTION_HEADER_BOLD: Final[re.Pattern[str]] = re.compile(r"^(\*\*(\d+)\.\*\*)(.*)$")
# Ordered list style used in current `final-exam.md` (plain `1.` … `45.`, not `**1.**`).
QUESTION_HEADER_PLAIN: Final[re.Pattern[str]] = re.compile(r"^(\d+)\.\s+(.*)$")

# Key table row matcher for extracting Part A answer letters.
KEY_ROW_RE: Final[re.Pattern[str]] = re.compile(r"^\|\s*(\d+)\s*\|\s*\*\*([ABCD])\*\*\s*\|")
