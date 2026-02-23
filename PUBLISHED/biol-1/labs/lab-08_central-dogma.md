# Lab 8: The Central Dogma — DNA to Protein

## Overview

The "Central Dogma" of molecular biology describes the directional flow of genetic information: from DNA to RNA to Protein. In this comprehensive lab, you will actively model these processes. By acting as the molecular machinery (RNA Polymerase and the Ribosome), you will transcribe a gene and translate it into a polypeptide chain. You will also model how genetic mutations alter the final protein product.

## Learning Objectives

By the end of this lab, you will be able to:

1. Model the process of Transcription (DNA → mRNA) using complementary base pairing rules.
2. Model the process of Translation (mRNA → Polypeptide) using a standard genetic code table.
3. Diagram the ribosome complex, including mRNA, tRNA, and amino acids.
4. Categorize mutations as substitutions, insertions, or deletions, and determine their effect on the reading frame (e.g., frameshift, missense, nonsense, silent).

## Materials

* Review Packet (this document)
* Standard Genetic Code (Codon Table) — Provided below
* Colored pencils

---

## Part 1: The Genetic Code Reference

Use this standard mRNA Codon Table to decode your transcripts in the following activities. To use the table: Find the first base on the left, the second base on the top, and the third base on the right.

| 1st Base | 2nd Base: U | 2nd Base: C | 2nd Base: A | 2nd Base: G | 3rd Base |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **U** | UUU (Phe/F)<br>UUC (Phe/F)<br>UUA (Leu/L)<br>UUG (Leu/L) | UCU (Ser/S)<br>UCC (Ser/S)<br>UCA (Ser/S)<br>UCG (Ser/S) | UAU (Tyr/Y)<br>UAC (Tyr/Y)<br>UAA **(STOP)**<br>UAG **(STOP)** | UGU (Cys/C)<br>UGC (Cys/C)<br>UGA **(STOP)**<br>UGG (Trp/W) | **U**<br>**C**<br>**A**<br>**G** |
| **C** | CUU (Leu/L)<br>CUC (Leu/L)<br>CUA (Leu/L)<br>CUG (Leu/L) | CCU (Pro/P)<br>CCC (Pro/P)<br>CCA (Pro/P)<br>CCG (Pro/P) | CAU (His/H)<br>CAC (His/H)<br>CAA (Gln/Q)<br>CAG (Gln/Q) | CGU (Arg/R)<br>CGC (Arg/R)<br>CGA (Arg/R)<br>CGG (Arg/R) | **U**<br>**C**<br>**A**<br>**G** |
| **A** | AUU (Ile/I)<br>AUC (Ile/I)<br>AUA (Ile/I)<br>AUG **(Met/M - START)**| ACU (Thr/T)<br>ACC (Thr/T)<br>ACA (Thr/T)<br>ACG (Thr/T) | AAU (Asn/N)<br>AAC (Asn/N)<br>AAA (Lys/K)<br>AAG (Lys/K) | AGU (Ser/S)<br>AGC (Ser/S)<br>AGA (Arg/R)<br>AGG (Arg/R) | **U**<br>**C**<br>**A**<br>**G** |
| **G** | GUU (Val/V)<br>GUC (Val/V)<br>GUA (Val/V)<br>GUG (Val/V) | GCU (Ala/A)<br>GCC (Ala/A)<br>GCA (Ala/A)<br>GCG (Ala/A) | GAU (Asp/D)<br>GAC (Asp/D)<br>GAA (Glu/E)<br>GAG (Glu/E) | GGU (Gly/G)<br>GGC (Gly/G)<br>GGA (Gly/G)<br>GGG (Gly/G) | **U**<br>**C**<br>**A**<br>**G** |

---

## Part 2: Transcription \& Translation Simulation

Act as **RNA Polymerase** to transcribe the given DNA Template Gene into mRNA. Remember the RNA base-pairing rules (A→U, T→A, C→G, G→C).

**Gene 1 (Normal Sequence):**

* **DNA Template Strand:** `T A C - C G T - A C G - T C G - G G T - G A C - A T C`

<!-- lab:reflection -->
**1. Transcribe the DNA strand into mRNA. Write the sequence by grouping it into 3-letter codons.**

{fill:textarea rows=2}

**2. Act as the Ribosome. Use the Codon Table above to translate your mRNA sequence into a chain of amino acids (a polypeptide). Use the 3-letter abbreviations (e.g., Met-Pro...).**

{fill:textarea rows=2}
<!-- /lab:reflection -->

---

## Part 3: Visualizing the translation machinery

Translation requires three major RNA players: mRNA (the message), tRNA (the transfer molecules carrying amino acids), and rRNA (the ribosome itself).

<!-- lab:drawing-area title="The Translation Complex" -->
**Draw a snapshot of Translation in progress.** Include and carefully label:

1. The **Ribosome** (Large and Small subunits)
2. The **mRNA** strand feeding through the ribosome
3. Two **tRNA** molecules inside the ribosome
4. An **Anticodon** on a tRNA matching with a **Codon** on the mRNA
5. The growing **Polypeptide Chain** (amino acids linked by peptide bonds) attached to a tRNA

{fill:drawing height=400}
<!-- /lab:drawing-area -->

<!-- lab:reflection -->
**3. If an mRNA codon is `C A U`, what must the tRNA anticodon be in order to deliver the correct amino acid?**

{fill:textarea rows=2}
<!-- /lab:reflection -->

---

## Part 4: Mutation Analysis

A mutation is a permanent change in the DNA sequence. Depending on where it happens and what type it is, it can have no effect, a minor effect, or a catastrophic effect on the resulting protein.

### Scenario A: Substitution (Point Mutation)

In Gene 1, the 8th DNA base (C) mutates into a (T).

* **Mutated DNA Template:** `T A C - C G T - A T G - T C G - G G T - G A C - A T C`

<!-- lab:reflection -->
**4. Transcribe and Translate this new sequence.**

* **Mutated mRNA:** {fill:text}
* **Mutated Protein:** {fill:text}

**5. What type of functional consequence did this substitution have? (Options: Silent, Missense, or Nonsense). Explain briefly.**

{fill:textarea rows=3}
<!-- /lab:reflection -->

### Scenario B: Frameshift (Insertion/Deletion)

Return to the original Gene 1. A replication error causes an extra Guanine (G) to be **inserted** directly after the very first TAC.

* **Mutated DNA Template:** `T A C - G C G - T A C - G T C - G G G - T G A - C A T - C...`

<!-- lab:reflection -->
**6. Transcribe and Translate this new frameshift sequence.**

* **Mutated mRNA:** {fill:text}
* **Mutated Protein:** {fill:text}

**7. Compare the impact of the Substitution mutation (Scenario A) to the Insertion mutation (Scenario B). Why are insertions and deletions generally considered more dangerous to an organism's phenotype?**

{fill:textarea rows=4}
<!-- /lab:reflection -->

## Conclusion

<!-- lab:reflection -->
**8. Explain how the Central Dogma connects an organism's *genotype* (its genetic instructions) to its *phenotype* (its physical traits).**

{fill:textarea rows=4}
<!-- /lab:reflection -->
