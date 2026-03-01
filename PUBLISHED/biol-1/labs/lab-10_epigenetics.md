# Lab 10: Epigenetics — Gene Regulation & Chromatin Control

## Overview

All cells in a multicellular organism contain the exact same DNA, yet a neuron looks and acts completely differently from a skin cell or a muscle cell. This specialization is possible because of **gene regulation**: the ability of a cell to turn specific genes "on" (expressed) or "off" (repressed) in response to internal signals or environmental conditions.

In this lab, you will explore gene regulation across two domains of life. First, you will model the classic *lac* operon system used by bacteria to rapidly adapt to their food source. Then, you will examine how eukaryotes use epigenetic modifications (like DNA methylation and histone acetylation) to achieve long-term cellular differentiation.

## Learning Objectives

By the end of this lab, you will be able to:

1. Identify the components of a bacterial operon (Promoter, Operator, Structural Genes, Repressor Protein).
2. Model how inducible operons (like the *lac* operon) use environmental cues to turn genes on/off.
3. Predict the consequences of specific mutations within the regulatory regions of an operon.
4. Diagram how epigenetic modifications alter chromatin structure to control eukaryotic gene accessibility.
5. Explain how environmental factors can influence gene expression through epigenetics.

## Materials

- Review Packet (this document)
- Colored pencils
- *Optional:* Paper cut-outs of the *lac* operon components (provided by instructor)

---

## Part 1: The Bacterial *lac* Operon

Bacteria like *E. coli* are highly efficient. If their preferred food (glucose) is unavailable, but a secondary food source (lactose) is present, they will suddenly turn on the genes required to digest lactose. This cluster of genes is called the *lac* operon.

The *lac* operon consists of:

- **Promoter:** Where RNA Polymerase binds to start transcription.
- **Operator:** The "on/off switch" where a Repressor protein can bind.
- **Structural Genes (lacZ, lacY, lacA):** The genes that code for the lactose-digesting enzymes.

### 1A. Modeling the "Off" State

When lactose is **absent**, the bacterium does not want to waste energy building enzymes to digest it.

<!-- lab:drawing-area title="The lac Operon (Lactose Absent)" -->
**Draw the *lac* operon in its repressed ("Off") state.**
Include and explicitly label:

1. The DNA strand with the **Promoter**, **Operator**, and **Structural Genes**.
2. **RNA Polymerase** attempting to bind to the promoter.
3. The **Active Repressor Protein** firmly bound to the Operator.
4. Show *why* RNA Polymerase cannot proceed (a physical roadblock).

{fill:drawing height=350}
<!-- /lab:drawing-area -->

### 1B. Modeling the "On" State (Induction)

When lactose is **present**, it acts as an *inducer*. It binds to the repressor protein, changing the repressor's shape (allosteric regulation) so it can no longer grip the operator DNA.

<!-- lab:drawing-area title="The lac Operon (Lactose Present)" -->
**Draw the *lac* operon in its induced ("On") state.**
Include and explicitly label:

1. The **Lactose molecule (Inducer)** bound to the **Repressor Protein**.
2. The Repressor detached from the Operator due to a shape change.
3. **RNA Polymerase** successfully binding the Promoter and moving across the Structural Genes.
4. The resulting **mRNA transcript** being created.

{fill:drawing height=350}
<!-- /lab:drawing-area -->

<!-- lab:reflection -->
**1. Why is the *lac* operon considered an "inducible" operon rather than a "repressible" operon? (Think about its default state).**

{fill:textarea rows=3}
<!-- /lab:reflection -->

---

## Part 2: Mutation Case Studies in the Operon

Mutations in the regulatory sequences (Promoter, Operator) or the Regulatory Gene (which makes the repressor) can have dramatic effects on the bacterium's ability to survive.

Analyze the following mutations and predict whether the structural genes (*lacZ, lacY, lacA*) will be **Always On (Constitutive)**, **Always Off (Repressed)**, or **Regulated Normally**.

<!-- lab:reflection -->
**Case Study A:** A mutation in the Operator sequence changes its shape, so the Repressor Protein can no longer bind to it under any circumstances.

- **Prediction (Always On, Always Off, or Normal)?** {fill:text}
- **Explanation:** {fill:textarea rows=2}

**Case Study B:** A mutation in the Promoter sequence prevents RNA Polymerase from recognizing and binding to it.

- **Prediction (Always On, Always Off, or Normal)?** {fill:text}
- **Explanation:** {fill:textarea rows=2}

**Case Study C:** A mutation in the Regulatory Gene creates a "Super-Repressor." This mutated repressor can still bind to the Operator, but it has lost the ability to bind to Lactose.

- **Prediction (Always On, Always Off, or Normal)?** {fill:text}
- **Explanation:** {fill:textarea rows=2}
<!-- /lab:reflection -->

---

## Part 3: Eukaryotic Regulation & Epigenetics

Unlike bacteria, eukaryotes do not typically use operons. Furthermore, eukaryotic DNA is tightly wrapped around protein spools called **histones** to form chromatin. If DNA is wrapped too tightly, RNA Polymerase cannot physically access the promoters.

Chemical tags can be added to the DNA or the histones to alter how tightly the DNA is packaged. This is called **Epigenetics** ("above genetics"), because it changes *expression* without changing the DNA sequence itself.

- **Methylation (Adding -CH₃ to DNA):** Causes chromatin to tightly condense. Turns genes **OFF**. (Heterochromatin).
- **Acetylation (Adding -COCH₃ to Histones):** Causes chromatin to loosen and spread apart. Turns genes **ON**. (Euchromatin).

<!-- lab:drawing-area title="Chromatin States" -->
**Draw two side-by-side diagrams:**

**Diagram A: Heterochromatin (Genes OFF)**
Show DNA tightly wound around histones with methyl groups (-CH₃) attached. Label the condensed state.

**Diagram B: Euchromatin (Genes ON)**
Show DNA loosely associated with histones with acetyl groups (-COCH₃) attached. Show RNA Polymerase accessing the promoter.

{fill:drawing height=350}
<!-- /lab:drawing-area -->

<!-- lab:reflection -->
**2. Imagine a skin cell and a neuron. Both contain the gene that codes for keratin (a tough skin protein) and the gene that codes for neurotransmitter receptors.**

- In the **skin cell**, which gene is likely highly *acetylated*, and which is highly *methylated*?
    1. Keratin Gene: {fill:text}
    2. Receptor Gene: {fill:text}

- In the **neuron**, which gene is likely highly *acetylated*, and which is highly *methylated*?
    1. Keratin Gene: {fill:text}
    2. Receptor Gene: {fill:text}

**3. Environmental factors like stress, diet, and toxins can alter a person's epigenetic tags, turning genes on or off over their lifetime. Identical twins have the exact same DNA sequence. Explain how epigenetic drift might cause identical twins to develop different traits or susceptibilities to disease as they age.**

{fill:textarea rows=5}
<!-- /lab:reflection -->

## Part 4: X-Inactivation — Epigenetics in Action

In female mammals, one X chromosome in each cell is randomly inactivated early in development, forming a condensed **Barr body**. This is an epigenetic process — the silenced X is heavily methylated.

<!-- lab:reflection -->
**4. Calico cats have patches of orange and black fur. The gene for coat color is on the X chromosome. Explain how random X-inactivation during embryonic development creates the mosaic pattern of a calico cat. Why are calico cats almost always female?**

{fill:textarea rows=5}
<!-- /lab:reflection -->

## Conclusion

<!-- lab:reflection -->
**5. Summarize the fundamental difference in strategies: How does a bacterium (using an operon) control gene expression compared to how a eukaryote (using epigenetics) controls gene expression?**

{fill:textarea rows=4}
<!-- /lab:reflection -->
