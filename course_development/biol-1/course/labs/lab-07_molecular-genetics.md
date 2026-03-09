# Lab 7: Molecular Genetics — From DNA to Protein

## Overview

Every living cell follows the same basic recipe to turn genetic information into a working molecule:

> **DNA → RNA → Protein**

This is the **Central Dogma** of molecular biology. It means your DNA is like a master cookbook that never leaves the kitchen (the nucleus). When a protein needs to be made, the cell copies just the recipe it needs into a messenger (mRNA), which travels to the ribosome — the cell's protein-building machine.

In this lab you will **be the cell**. You'll copy DNA into mRNA (*transcription*), decode mRNA into amino acids (*translation*), and discover what happens when the recipe gets a typo (*mutations*).

## Learning Objectives

By the end of this lab, you will be able to:

1. Transcribe a DNA sequence into mRNA using base-pairing rules.
2. Translate an mRNA sequence into amino acids using a codon table.
3. Predict the effects of point mutations and frameshift mutations on a protein.
4. Explain the Central Dogma in your own words.

## Materials

- This worksheet
- Codon table (Part 1)
- Colored pencils (optional — great for color-coding bases!)

---

<div style="page-break-after: always;"></div>

## Part 1: The Codon Table

mRNA is read in groups of **three bases** called **codons**. Each codon specifies one amino acid (or a stop signal). The table below lists all 64 codons.

> **How to use it:** Find the first base in the left column, the second base in the top row, and the third base in the right column. The intersection gives you the amino acid.

| | **U** | **C** | **A** | **G** | |
|:---:|:---:|:---:|:---:|:---:|:---:|
| | *2nd base →* | | | | *3rd base ↓* |
| **U** | **Phe** (F) | **Ser** (S) | **Tyr** (Y) | **Cys** (C) | **U** |
| | **Phe** (F) | **Ser** (S) | **Tyr** (Y) | **Cys** (C) | **C** |
| | **Leu** (L) | **Ser** (S) | ⛔ STOP | ⛔ STOP | **A** |
| | **Leu** (L) | **Ser** (S) | ⛔ STOP | **Trp** (W) | **G** |
| **C** | **Leu** (L) | **Pro** (P) | **His** (H) | **Arg** (R) | **U** |
| | **Leu** (L) | **Pro** (P) | **His** (H) | **Arg** (R) | **C** |
| | **Leu** (L) | **Pro** (P) | **Gln** (Q) | **Arg** (R) | **A** |
| | **Leu** (L) | **Pro** (P) | **Gln** (Q) | **Arg** (R) | **G** |
| **A** | **Ile** (I) | **Thr** (T) | **Asn** (N) | **Ser** (S) | **U** |
| | **Ile** (I) | **Thr** (T) | **Asn** (N) | **Ser** (S) | **C** |
| | **Ile** (I) | **Thr** (T) | **Lys** (K) | **Arg** (R) | **A** |
| | 🟢 **Met** (M) START | **Thr** (T) | **Lys** (K) | **Arg** (R) | **G** |
| **G** | **Val** (V) | **Ala** (A) | **Asp** (D) | **Gly** (G) | **U** |
| | **Val** (V) | **Ala** (A) | **Asp** (D) | **Gly** (G) | **C** |
| | **Val** (V) | **Ala** (A) | **Glu** (E) | **Gly** (G) | **A** |
| | **Val** (V) | **Ala** (A) | **Glu** (E) | **Gly** (G) | **G** |

> **Key:**
>
> - 🟢 **AUG** = Start codon (also codes for Methionine)
> - ⛔ **UAA, UAG, UGA** = Stop codons (no amino acid added — translation ends)

### Quick Practice

Try decoding these three codons before moving on:

| Codon | 1st base | 2nd base | 3rd base | Amino Acid |
|:---:|:---:|:---:|:---:|:---:|
| GCA | G | C | A | __________ |
| UUU | U | U | U | __________ |
| AUG | A | U | G | __________ |

---

<div style="page-break-after: always;"></div>

## Part 2: Transcription & Translation

### Background

Think of transcription like photocopying one page from a master binder — the original DNA stays safe in the nucleus while the mRNA copy travels to the ribosome.

**Base-pairing rules for transcription (DNA → mRNA):**

| DNA base | mRNA base |
|:---:|:---:|
| A | U |
| T | A |
| G | C |
| C | G |

### Your Gene

**DNA template strand:**

`3′ — T A C · C G T · A C G · T C G · G G T · G A C · A T T — 5′`

<!-- lab:reflection -->
**1. Transcribe — Write the mRNA sequence. Group into codons (groups of 3).**

{fill:textarea rows=2}

**2. Translate — Use the codon table to convert each codon into an amino acid. Write the amino acid chain.**

{fill:textarea rows=2}

**3. What was your first codon? What amino acid does it code for, and why is that codon special?**

{fill:text}

**4. How did you know to stop translating? What was the stop codon?**

{fill:text}
<!-- /lab:reflection -->

---

<div style="page-break-after: always;"></div>

## Part 3: Mutation Detective

Mutations are changes in the DNA sequence — like typos in a recipe. Some are harmless; others can ruin the dish. Let's investigate.

Go back to the **original DNA template strand** from Part 2.

### Scenario A: Substitution (Point Mutation)

The **10th base** (the first `C` in the third codon `ACG`) changes to a **C → G**.

**Mutated DNA template:** `3′ — T A C · C G T · A G G · T C G · G G T · G A C · A T T — 5′`

<!-- lab:reflection -->
**5. Transcribe and translate the mutated sequence.**

- Mutated mRNA: {fill:text}
- Amino acid chain: {fill:text}

**6. Did the amino acid chain change? Classify the mutation as *silent* (no change), *missense* (different amino acid), or *nonsense* (creates a premature stop).**

{fill:textarea rows=2}
<!-- /lab:reflection -->

### Scenario B: Insertion (Frameshift Mutation)

Return to the **original DNA template**. An extra **G** is inserted right after the 3rd base (after the `C` in `TAC`).

**Mutated DNA template:** `3′ — T A C · G C G · T A C · G T C · G G G · T G A · C A T · T — 5′`

<!-- lab:reflection -->
**7. Transcribe and translate the frameshift-mutated sequence.**

- Mutated mRNA: {fill:text}
- Amino acid chain: {fill:text}

**8. Compare the frameshift protein to your original. How many amino acids changed? Why is this type called a "frameshift"?**

{fill:textarea rows=3}

**9. Which mutation was more damaging — the substitution (A) or the frameshift (B)? Explain your reasoning.**

{fill:textarea rows=3}
<!-- /lab:reflection -->

---

## Part 4: Big Picture

<!-- lab:reflection -->
**10. Complete the Central Dogma:**

DNA → _________________ → _________________

**11. Where in a eukaryotic cell does transcription occur?**

{fill:text}

**12. Where does translation occur?**

{fill:text}

**13. What enzyme copies DNA into mRNA (carries out transcription)?**

{fill:text}

**14. What cellular structure reads mRNA and builds proteins (carries out translation)?**

{fill:text}

**15. In your own words: How can a single change in someone's DNA affect their physical traits? Trace the path from gene → protein → trait.**

{fill:textarea rows=4}
<!-- /lab:reflection -->
