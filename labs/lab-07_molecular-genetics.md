# Lab 7: Molecular Genetics — From DNA to Protein

**BIOL-1: General Biology** | College of the Redwoods, Pelican Bay

**Name:** {fill:text} **Date:** {fill:text}

---

## Learning Objectives

By the end of this lab, you will be able to:

1. Transcribe a DNA sequence into mRNA using base-pairing rules.
2. Translate an mRNA sequence into amino acids using a codon table.
3. Predict the effects of point mutations and frameshift mutations on a protein.
4. Explain the Central Dogma in your own words.

## Overview

Every living cell follows the same basic recipe to turn genetic information into a working molecule:

> **DNA → RNA → Protein**

This is the **Central Dogma** of molecular biology. It means your DNA is like a master cookbook that never leaves the kitchen (the nucleus). When a protein needs to be made, the cell copies just the recipe it needs into a messenger (mRNA), which travels to the ribosome — the cell's protein-building machine.

In this lab you will **be the cell**. You'll copy DNA into mRNA (*transcription*), decode mRNA into amino acids (*translation*), and discover what happens when the recipe gets a typo (*mutations*).

## Materials

- This worksheet
- Codon table (Part 1)
- Colored pencils (optional — great for color-coding bases!)

---

<div style="page-break-after: always;"></div>

## Part 1: Base Pairing — The Language of DNA and RNA

DNA and RNA are built from four **nucleotide bases**. These bases always pair in specific, predictable ways — like puzzle pieces that only fit together one way. Understanding these pairing rules is the key to everything else in this lab.

### DNA–DNA Pairing (Replication)

When a cell needs to **copy its DNA** before dividing, the double helix unzips and each strand serves as a template. The enzyme **DNA Polymerase** reads the template and adds the matching base according to these rules:

| Template Base | Pairs With |
|:---:|:---:|
| **A** (Adenine) | **T** (Thymine) |
| **T** (Thymine) | **A** (Adenine) |
| **G** (Guanine) | **C** (Cytosine) |
| **C** (Cytosine) | **G** (Guanine) |

> 🧠 **Memory trick:** **A**lways with **T**, **G**oes with **C** — in DNA, A pairs with T and G pairs with C.

**Quick practice — Write the complementary DNA strand:**

| Template | T | A | C | C | G | T |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| New strand | ___ | ___ | ___ | ___ | ___ | ___ |

### DNA–RNA Pairing (Transcription)

When the cell needs to **make a protein**, it doesn't send the DNA out of the nucleus. Instead, the enzyme **RNA Polymerase** reads the DNA template and builds a single-stranded **mRNA** (messenger RNA) copy — a process called **transcription**.

RNA has one important difference: it uses **Uracil (U)** instead of Thymine (T).

| DNA Template Base | Pairs With (RNA) |
|:---:|:---:|
| **A** (Adenine) | **U** (Uracil) |
| **T** (Thymine) | **A** (Adenine) |
| **G** (Guanine) | **C** (Cytosine) |
| **C** (Cytosine) | **G** (Guanine) |

> 🔑 **The only change from DNA→DNA pairing:** Wherever DNA has **A**, the mRNA gets **U** instead of T. Everything else stays the same.

**Quick practice — Transcribe this short DNA template into mRNA:**

| DNA Template | T | A | C | C | G | T |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| mRNA | ___ | ___ | ___ | ___ | ___ | ___ |

<!-- lab:reflection -->
**Check your understanding:**

**1. What are the two base-pairing rules that are the *same* in both DNA replication and transcription?**

{fill:text}

**2. What is the one key difference between DNA–DNA pairing and DNA–RNA pairing?**

{fill:text}

**3. If a DNA template strand reads `G-A-T-T-C-A`, what would the mRNA sequence be?**

{fill:text}
<!-- /lab:reflection -->

---

<div style="page-break-after: always;"></div>

## Part 2: Transcription — DNA → mRNA

Now let's apply those pairing rules to a full gene! Transcription is like photocopying one page from a master binder — the original DNA stays safe in the nucleus while the mRNA copy travels to the ribosome.

Use the DNA→RNA pairing rules from Part 1: **A→U, T→A, G→C, C→G**.

**DNA template strand:** `3′ — T A C · C G T · A C G · T C G · G G T · G A C · A T T — 5′`

<!-- lab:reflection -->
**4. Transcribe — Write the mRNA sequence. Group into codons (groups of 3).**

{fill:textarea rows=2}

**5. Where in a eukaryotic cell does transcription occur?**

{fill:text}

**6. What enzyme carries out transcription?**

{fill:text}
<!-- /lab:reflection -->

---

<div style="page-break-after: always;"></div>

## Part 3: Translation — mRNA → Protein (The Codon Table)

Once the mRNA reaches the ribosome, it is read in groups of **three bases** called **codons**. Each codon specifies one amino acid (or a stop signal). This process is called **translation** — the cell is literally *translating* the language of nucleotides into the language of amino acids.

### The Codon Table

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

<!-- lab:reflection -->
**7. Translate your mRNA from Part 2 — Use the codon table to convert each codon into an amino acid. Write the amino acid chain.**

{fill:textarea rows=2}

**8. What was your first codon? What amino acid does it code for, and why is that codon special?**

{fill:text}

**9. How did you know to stop translating? What was the stop codon?**

{fill:text}

**Bonus look-up:** Find two different codons that both code for Leucine (Leu). Write them here:

{fill:text}

This is called **redundancy** — multiple codons can code for the same amino acid. Why might this be useful for an organism? *(Hint: think about mutations.)*

{fill:textarea rows=2}
<!-- /lab:reflection -->

---

<div style="page-break-after: always;"></div>

## Part 4: Mutation Detective

Mutations are changes in the DNA sequence — like typos in a recipe. Some are harmless; others can ruin the dish. Let's investigate.

Go back to the **original DNA template strand** from Part 2.

### Scenario A: Substitution (Point Mutation)

The **10th base** (the first `C` in the third codon `ACG`) changes to a **C → G**.

**Mutated DNA template:** `3′ — T A C · C G T · A G G · T C G · G G T · G A C · A T T — 5′`

<!-- lab:reflection -->
**10. Transcribe and translate the mutated sequence.**

- Mutated mRNA: {fill:text}
- Amino acid chain: {fill:text}

**11. Did the amino acid chain change? Classify the mutation as *silent* (no change), *missense* (different amino acid), or *nonsense* (creates a premature stop).**

{fill:textarea rows=2}
<!-- /lab:reflection -->

### Scenario B: Insertion (Frameshift Mutation)

Return to the **original DNA template**. An extra **G** is inserted right after the 3rd base (after the `C` in `TAC`).

**Mutated DNA template:** `3′ — T A C · G C G · T A C · G T C · G G G · T G A · C A T · T — 5′`

<!-- lab:reflection -->
**12. Transcribe and translate the frameshift-mutated sequence.**

- Mutated mRNA: {fill:text}
- Amino acid chain: {fill:text}

**13. Compare the frameshift protein to your original. How many amino acids changed? Why is this type called a "frameshift"?**

{fill:textarea rows=3}
<!-- /lab:reflection -->

### Scenario C: Deletion (Another Frameshift)

Return to the **original DNA template**. This time, **delete the 7th base** (the `T` in the second codon `CGT`).

**Mutated DNA template:** `3′ — T A C · C G A · C G · T C G · G G T · G A C · A T T — 5′`

*(Re-group into codons after the deletion:)* `3′ — T A C · C G A · C G T · C G G · G T G · A C A · T T — 5′`

<!-- lab:reflection -->
**14. Transcribe and translate the deletion-mutated sequence.**

- Mutated mRNA: {fill:text}
- Amino acid chain: {fill:text}

**15. How does a deletion compare to an insertion? Did both cause the same amount of damage to the protein?**

{fill:textarea rows=2}
<!-- /lab:reflection -->

### Comparing All Three Mutations

<!-- lab:reflection -->
**16. Rank the three mutations (substitution, insertion, deletion) from least to most damaging. Explain your reasoning.**

{fill:textarea rows=3}
<!-- /lab:reflection -->

---

## Part 5: Big Picture

<!-- lab:reflection -->
**17. Complete the Central Dogma:**

DNA → _________________ → _________________

**18. Where in a eukaryotic cell does transcription occur?**

{fill:text}

**19. Where does translation occur?**

{fill:text}

**20. What cellular structure reads mRNA and builds proteins (carries out translation)?**

{fill:text}

**21. In your own words: How can a single change in someone's DNA affect their physical traits? Trace the path from gene → protein → trait.**

{fill:textarea rows=4}
<!-- /lab:reflection -->

---

## Part 6: Real-World Connection

<!-- lab:reflection -->
**22. Sickle-cell disease** is caused by a single point mutation in the hemoglobin gene. The 6th amino acid changes from Glutamic acid (Glu) to Valine (Val). Based on what you learned today:

- What kind of mutation is this — silent, missense, or nonsense? {fill:text}
- Why can a single amino acid change affect the shape of an entire protein? *(Hint: amino acids fold into 3D shapes, and each one contributes to the fold.)*

{fill:textarea rows=3}

**23. Not all mutations are bad!** Can you think of a situation where a mutation might actually help an organism survive? *(Hint: think about how evolution works.)*

{fill:textarea rows=3}
<!-- /lab:reflection -->

---

## Bonus Challenge 🧬

<!-- lab:reflection -->
**Design your own mutation!** Start with the original DNA template from Part 2. Create a mutation of your choice (substitution, insertion, or deletion), then transcribe and translate it.

- Type of mutation you chose: {fill:text}
- Your mutated DNA template: {fill:text}
- Mutated mRNA: {fill:text}
- Amino acid chain: {fill:text}
- What happened to the protein? Was it silent, missense, nonsense, or a frameshift? {fill:text}
<!-- /lab:reflection -->
