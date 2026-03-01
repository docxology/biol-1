# Lab 11: Genomics & Biotechnology

## Overview

Biotechnology is the application of molecular biology techniques to solve problems and create useful products. In this lab, you will work through the core techniques of modern molecular genetics: cutting and pasting DNA with restriction enzymes, amplifying DNA with PCR, separating fragments by gel electrophoresis, and analyzing the results. You will apply these techniques to real-world scenarios including forensic DNA profiling, genetic engineering, and gene therapy.

## Learning Objectives

By the end of this lab, you will be able to:

1. Diagram how restriction enzymes cut DNA and how DNA ligase joins fragments to create recombinant DNA.
2. Model the three steps of PCR (Polymerase Chain Reaction) and explain why each step is necessary.
3. Predict the migration pattern of DNA fragments in gel electrophoresis based on fragment size.
4. Analyze a simulated DNA fingerprint to solve a forensic or paternity scenario.
5. Evaluate the benefits and ethical considerations of genetic engineering and gene therapy.

## Materials

- Review Packet (this document)
- Colored pencils
- Ruler (for gel electrophoresis diagram)
- Scratch paper

---

## Part 1: Restriction Enzymes & Recombinant DNA

Restriction enzymes are molecular "scissors" that cut DNA at specific recognition sequences. When two DNA samples are cut with the same restriction enzyme, they produce compatible ends that can be joined together by DNA ligase.

<!-- lab:drawing-area title="Creating Recombinant DNA" -->
**Diagram the following process step by step:**

1. Draw a **circular bacterial plasmid** with a single restriction site (EcoRI: GAATTC).
2. Draw a **linear piece of human DNA** containing the insulin gene, flanked by two EcoRI sites.
3. Show both being cut by **EcoRI**, producing **sticky ends**.
4. Show the human insulin gene being **inserted** into the opened plasmid.
5. Show **DNA ligase** sealing the joins to create **recombinant DNA**.

{fill:drawing height=400}
<!-- /lab:drawing-area -->

<!-- lab:reflection -->
**1. Why are "sticky ends" more useful than "blunt ends" for creating recombinant DNA? What property allows matching sticky ends to bind together temporarily before ligase seals them?**

{fill:textarea rows=3}

**2. If a plasmid has one EcoRI site and the donor DNA has two EcoRI sites flanking the gene of interest, how many DNA fragments are produced from the donor DNA after digestion?**

{fill:textarea rows=2}
<!-- /lab:reflection -->

---

## Part 2: PCR — The Molecular Photocopier

PCR (Polymerase Chain Reaction) is a technique that can amplify a tiny sample of DNA into millions of copies in just a few hours. It uses three repeated temperature cycles.

<!-- lab:reflection -->
**3. Fill in the table describing the three steps of each PCR cycle:**

| Step | Temperature | What Happens | Why This Temperature? |
| :--- | :---: | :--- | :--- |
| **1. Denaturation** | ~95°C | | |
| **2. Annealing** | ~55°C | | |
| **3. Extension** | ~72°C | | |

{fill:textarea rows=5}

**4. PCR uses a special heat-stable DNA polymerase called *Taq* polymerase, originally isolated from *Thermus aquaticus*, a bacterium that lives in hot springs. Why is heat stability essential for this enzyme? What would happen if a normal human DNA polymerase were used instead?**

{fill:textarea rows=3}

**5. Starting with a single molecule of DNA, how many copies would you have after 10 complete PCR cycles? (Hint: Each cycle doubles the number of copies. Use the formula $2^n$ where n = number of cycles.)**

{fill:textarea rows=2}
<!-- /lab:reflection -->

---

## Part 3: Gel Electrophoresis — Sorting by Size

Gel electrophoresis separates DNA fragments by size using an electric field. DNA is negatively charged (due to phosphate groups), so it migrates toward the positive electrode. Smaller fragments move faster and farther through the gel matrix.

<!-- lab:drawing-area title="Gel Electrophoresis Results" -->
**Draw a gel electrophoresis result.** Include:

1. Wells at the top of the gel (loading end, negative electrode)
2. The positive electrode at the bottom
3. A **DNA Ladder** (molecular weight standard) in Lane 1 with bands at: 10,000 bp, 5,000 bp, 2,000 bp, 1,000 bp, 500 bp
4. **Sample A** in Lane 2 with bands at approximately 5,000 bp and 2,000 bp
5. **Sample B** in Lane 3 with bands at approximately 5,000 bp, 1,000 bp, and 500 bp

{fill:drawing height=350}
<!-- /lab:drawing-area -->

<!-- lab:reflection -->
**6. A restriction enzyme cuts Sample A into two fragments and Sample B into three fragments. Based on your gel drawing, which sample has a larger total DNA size? (Add up the fragment sizes for each sample.)**

{fill:textarea rows=2}
<!-- /lab:reflection -->

---

## Part 4: DNA Fingerprinting — A Forensic Application

DNA fingerprinting compares **Short Tandem Repeats (STRs)** — highly variable regions of DNA where a short sequence (e.g., AGAT) is repeated a differing number of times between individuals. Because everyone (except identical twins) has a unique pattern of STR lengths, this technique can identify individuals.

**Scenario:** A crime scene hair sample is analyzed along with DNA from three suspects. The STR profiles are run on a gel.

<!-- lab:reflection -->
**7. The crime scene sample shows bands at positions matching exactly two of the bands from Suspect 2 and none from Suspects 1 or 3. Can you positively identify Suspect 2 as the source of the hair? What additional evidence or testing might strengthen this conclusion?**

{fill:textarea rows=3}

**8. In a paternity test, a child has STR bands at positions A, B, C, and D. The mother has bands at A and C. Which bands *must* have come from the biological father? If Potential Father 1 has bands at B and E (but not D), can he be the biological father? Explain.**

{fill:textarea rows=4}
<!-- /lab:reflection -->

---

## Part 5: Genetic Engineering & Gene Therapy

<!-- lab:reflection -->
**9. Golden Rice is a transgenic crop engineered to produce beta-carotene (Vitamin A precursor) in the rice grain. Describe the general steps scientists would use to create this GMO, starting from identifying the beta-carotene gene in daffodils and ending with a rice plant that produces golden grains. Use the vocabulary: restriction enzyme, plasmid, DNA ligase, transformation.**

{fill:textarea rows=5}

**10. Gene therapy aims to treat genetic diseases by introducing a functional copy of a defective gene into a patient's cells. Compare *ex vivo* gene therapy (cells removed, treated, returned) with *in vivo* gene therapy (treatment delivered directly into the body). What are the advantages and challenges of each approach?**

{fill:textarea rows=5}
<!-- /lab:reflection -->

## Conclusion

<!-- lab:reflection -->
**11. The genetic code is nearly universal — the same codons specify the same amino acids in bacteria, plants, and humans. Explain how this universality makes biotechnology possible. Specifically, why can a bacterial cell read a human insulin gene and produce functional human insulin?**

{fill:textarea rows=4}

**12. CRISPR-Cas9 is a new gene-editing tool that allows precise cuts at specific DNA sequences. Unlike older methods, CRISPR can edit genes *in place* rather than inserting new ones. Discuss one potential medical application and one ethical concern related to using CRISPR to edit human embryos.**

{fill:textarea rows=4}
<!-- /lab:reflection -->
