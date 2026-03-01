# Lab 7: Molecular Genetics — From DNA to Protein

## Overview

The "Central Dogma" of molecular biology describes how the information in your genes becomes a working part of your body: **DNA → RNA → Protein**. Every protein in every cell — from the keratin in your hair to the hemoglobin carrying oxygen in your blood — was built by reading a gene through this pathway.

In this lab, you will act as the cell's molecular machinery. You will **transcribe** a gene (copy DNA into mRNA) and then **translate** that mRNA into a chain of amino acids using the genetic code. You will also see firsthand how **mutations** — even small changes in the DNA — can alter the protein product.

## Learning Objectives

By the end of this lab, you will be able to:

1. Transcribe a DNA sequence into mRNA using base pairing rules.
2. Translate an mRNA sequence into amino acids using a codon table.
3. Identify the effects of point mutations and frameshift mutations on a protein.
4. Explain why the Central Dogma matters for understanding genetics.

## Materials

- This worksheet
- Codon table (provided in Part 1)
- Colored pencils (optional)

---

<div style="page-break-after: always;"></div>

## Part 1: The Genetic Code Reference

Use this mRNA codon table to decode your mRNA sequences. **How to read it:** Find the 1st base on the left, the 2nd base across the top, and the 3rd base on the right.

| 1st Base | U | C | A | G | 3rd Base |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **U** | Phe (F) / Phe (F) / Leu (L) / Leu (L) | Ser (S) / Ser (S) / Ser (S) / Ser (S) | Tyr (Y) / Tyr (Y) / **STOP** / **STOP** | Cys (C) / Cys (C) / **STOP** / Trp (W) | U / C / A / G |
| **C** | Leu (L) / Leu (L) / Leu (L) / Leu (L) | Pro (P) / Pro (P) / Pro (P) / Pro (P) | His (H) / His (H) / Gln (Q) / Gln (Q) | Arg (R) / Arg (R) / Arg (R) / Arg (R) | U / C / A / G |
| **A** | Ile (I) / Ile (I) / Ile (I) / **Met (M) START** | Thr (T) / Thr (T) / Thr (T) / Thr (T) | Asn (N) / Asn (N) / Lys (K) / Lys (K) | Ser (S) / Ser (S) / Arg (R) / Arg (R) | U / C / A / G |
| **G** | Val (V) / Val (V) / Val (V) / Val (V) | Ala (A) / Ala (A) / Ala (A) / Ala (A) | Asp (D) / Asp (D) / Glu (E) / Glu (E) | Gly (G) / Gly (G) / Gly (G) / Gly (G) | U / C / A / G |

> **Tip:** Each cell shows 4 amino acids separated by slashes, corresponding to 3rd base = U, C, A, G (top to bottom).

> **Remember:** AUG is both the Start codon AND codes for Methionine (Met). UAA, UAG, UGA are Stop codons.

---

## Part 2: Transcription and Translation

*Transcription is like copying one page from a library book — the original DNA stays in the nucleus, and the mRNA copy travels to the ribosome.*

**Your gene (DNA template strand):** `3′ — T A C · C G T · A C G · T C G · G G T · G A C · A T T — 5′`

**Base pairing rules for transcription:** A → U, T → A, G → C, C → G

<!-- lab:reflection -->
**1. Transcribe: Write the mRNA sequence by replacing each DNA base with its RNA complement. Group into codons (3 letters each).**

{fill:textarea rows=2}

**2. Translate: Use the codon table to convert each mRNA codon into an amino acid. Write the amino acid chain.**

{fill:textarea rows=2}

**3. Which codon did you start with? What amino acid does it code for?**

{fill:text}

**4. What told you to stop translating? What was the stop codon?**

{fill:text}
<!-- /lab:reflection -->

---

<div style="page-break-after: always;"></div>

## Part 3: Mutation Analysis

*Mutations are changes in the DNA sequence. Some are harmless; others can be devastating. Let's see why.*

Return to the **original DNA template strand** from Part 2.

### Scenario A: Point Mutation (Substitution)

The **10th base** (the first T in the third codon `ACG`) changes to a **G**.

New DNA template: `3′ — T A C · C G T · A G G · T C G · G G T · G A C · A T T — 5′`

<!-- lab:reflection -->
**5. Transcribe and translate the mutated sequence.**

- Mutated mRNA: {fill:text}
- Mutated amino acids: {fill:text}

**6. Did the amino acid chain change compared to your original? What type of mutation is this — silent, missense, or nonsense?**

{fill:textarea rows=2}
<!-- /lab:reflection -->

### Scenario B: Frameshift Mutation (Insertion)

Return to the **original DNA template**. An extra **G** is inserted right after the 3rd base (after the `C` in `TAC`).

New DNA template: `3′ — T A C · G C G · T A C · G T C · G G G · T G A · C A T · T — 5′`

<!-- lab:reflection -->
**7. Transcribe and translate the mutated sequence.**

- Mutated mRNA: {fill:text}
- Mutated amino acids: {fill:text}

**8. Compare your frameshift protein to your original protein. How many amino acids changed? Why is this called a "frameshift"?**

{fill:textarea rows=3}

**9. Which type of mutation is more dangerous — the point mutation (Scenario A) or the frameshift (Scenario B)? Explain why.**

{fill:textarea rows=3}
<!-- /lab:reflection -->

---

## Part 4: Putting It All Together

<!-- lab:reflection -->
**10. Fill in the Central Dogma:**

DNA → _________________ → _________________

**11. Where does transcription happen in a eukaryotic cell?**

{fill:text}

**12. Where does translation happen?**

{fill:text}

**13. What enzyme carries out transcription?**

{fill:text}

**14. What structure carries out translation?**

{fill:text}

**15. In your own words, explain why a change in DNA can change what a person looks like or how their body works. (Hint: trace the path from gene to trait.)**

{fill:textarea rows=4}
<!-- /lab:reflection -->
