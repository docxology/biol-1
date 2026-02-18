# Lab 8: Genetics & Inheritance

**BIOL-8: Human Biology** | College of the Redwoods, Del Norte Campus

---

**Name:** {fill:text} **Date:** {fill:text}

---

## Objectives

By the end of this lab, you will be able to:

- **Apply the laws of probability** to genetic inheritance using coin tosses
- **Perform monohybrid crosses** to predict genotype and phenotype ratios
- **Demonstrate independent assortment** using dihybrid crosses (simulation)
- **Analyze human pedigrees** to determine inheritance patterns (dominant vs. recessive, autosomal vs. sex-linked)
- **Solve genetics problems** involving sex-linked traits and multiple alleles (blood types)

---

## Introduction

**Genetics** is the scientific study of heredity—how traits are passed from parents to offspring. The fundamental unit of heredity is the **gene**, a segment of DNA that codes for a specific protein or trait. Genes come in different versions called **alleles**.

### Key Terminology

| Term | Definition |
|------|------------|
| **Genotype** | The genetic makeup of an organism (e.g., *AA*, *Aa*, *aa*) |
| **Phenotype** | The physical expression of the trait (e.g., *Purple flowers*, *White flowers*) |
| **Homozygous** | Having two identical alleles for a trait (*AA* or *aa*) |
| **Heterozygous** | Having two different alleles for a trait (*Aa*) |
| **Dominant** | An allele that masks the presence of a recessive allele (represented by capital letters) |
| **Recessive** | An allele that is only expressed when two copies are present (represented by lowercase letters) |

In this lab, you will simulate genetic crosses, analyze real human traits, and practice predicting outcomes using **Punnett squares**.

---

## Materials

- Two coins (pennies or nickels) per pair of students
- Calculator
- Colored pencils (optional)

## Safety Considerations

- None. This is a simulation and paper-based lab.

---

## Part 1: Probability and Genetics

> **Learning Goal:** Understand how random chance determines which alleles are passed to offspring.

Sexual reproduction involves chance. During meiosis, homologous chromosomes separate (segregate), so a parent passes only *one* of their two alleles to their offspring. Which one they pass is random—like flipping a coin.

### Procedure: The Coin Toss

Imagine a parent is **heterozygous (Aa)** for a trait.

- **Heads** = Dominant allele (**A**)
- **Tails** = Recessive allele (**a**)

1. **Get two coins.** One represents the **Father (Aa)**, the other represents the **Mother (Aa)**.
2. **Flip both coins simultaneously** 50 times.
3. Record the combination for each toss in the tally table below.
   - **Heads/Heads** = **AA** (Homozygous Dominant)
   - **Heads/Tails** = **Aa** (Heterozygous)
   - **Tails/Tails** = **aa** (Homozygous Recessive)

### Data Collection

<!-- lab:data-table rows=4 title="Genotype Tally Sheet (50 Tosses)" -->
| Genotype | Tally (mark each toss) | Total Count | Percentage (Count ÷ 50 × 100) |
|---|---|---|---|
| **AA** (Heads/Heads) | {fill:text} | {fill:number} | {fill:number}% |
| **Aa** (Heads/Tails) | {fill:text} | {fill:number} | {fill:number}% |
| **aa** (Tails/Tails) | {fill:text} | {fill:number} | {fill:number}% |
<!-- /lab:data-table -->

### Analysis

<!-- lab:reflection -->
**1. Theoretically, in a cross between two heterozygotes (Aa × Aa), the expected ratio is 25% AA, 50% Aa, and 25% aa. How close were your results to these percentages?**

{fill:textarea rows=2}

**2. Why might your actual results differ slightly from the theoretical expectation?**

{fill:textarea rows=2}
<!-- /lab:reflection -->

---

## Part 2: Monohybrid Crosses

> **Learning Goal:** Use Punnett squares to predict offspring for a single trait.

### Scenario: Albinism in Humans

Albinism (lack of skin pigment) is an **autosomal recessive** condition.

- **A** = Normal pigmentation (Dominant)
- **a** = Albinism (Recessive)

**Problem 1:** A man who is **homozygous dominant (AA)** has children with a woman who is **albino (aa)**.

1. Draw the Punnett square:

```
      __a__   __a__
    |       |       |
  A |   ?   |   ?   |
    |_______|_______|
    |       |       |
  A |   ?   |   ?   |
    |_______|_______|
```

<!-- lab:reflection -->
**What is the genotype of all offspring?**
{fill:text}

**What is the phenotype of all offspring?**
{fill:text}
<!-- /lab:reflection -->

**Problem 2:** Now, suppose one of the children from the cross above (who is **heterozygous Aa**) marries another person who is also **heterozygous (Aa)**.

<!-- lab:reflection -->
**Draw the Punnett square for Aa × Aa.**

**What are the expected genotypic percentages?**

- AA: {fill:text}%
- Aa: {fill:text}%
- aa: {fill:text}%

**What is the probability (as a fraction) that they will have an albino child?**
{fill:text}
<!-- /lab:reflection -->

---

## Part 3: Dihybrid Crosses (Independent Assortment)

> **Learning Goal:** Track two traits at once to see how they sort independently.

Mendel's **Law of Independent Assortment** states that different gene pairs segregate independently during gamete formation (as long as they are on different chromosomes).

### Scenario: Peas

We will look at two traits in pea plants:

1. **Seed Shape**: Round (**R**) is dominant to Wrinkled (**r**)
2. **Seed Color**: Yellow (**Y**) is dominant to Green (**y**)

**Cross:** Two parents are heterozygous for *both* traits: **RrYy × RrYy**.

### Procedure

1. Determine the possible gametes each parent can produce using the **FOIL** method (First, Outer, Inner, Last).
   - Parent alleles: **R r Y y**
   - Gametes: **RY**, **Ry**, **rY**, **ry**

2. Complete the 16-square Punnett square below.

<!-- lab:data-table rows=5 title="Dihybrid Cross: RrYy × RrYy" -->
| | RY | Ry | rY | ry |
|---|---|---|---|---|
| **RY** | RRYY | RRYy | RrYY | RrYy |
| **Ry** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **rY** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **ry** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
<!-- /lab:data-table -->

### Analysis

Count the phenotypes in your table to find the famous **9:3:3:1 ratio**.

<!-- lab:reflection -->
**How many are Round & Yellow (R_Y_)?**
{fill:number} / 16

**How many are Round & Green (R_yy)?**
{fill:number} / 16

**How many are Wrinkled & Yellow (rrY_)?**
{fill:number} / 16

**How many are Wrinkled & Green (rryy)?**
{fill:number} / 16
<!-- /lab:reflection -->

---

## Part 4: Human Genetic Traits

> **Learning Goal:** Observe dominant and recessive traits in yourself and classmates.

Many human traits are complex and polygenic, but some behave (mostly) like simple Mendelian traits.

1. **Tongue Rolling**: Dominant (**T** = can roll); Recessive (**t** = cannot)
2. **Attached Earlobes**: Dominant (**E** = unattached/free); Recessive (**e** = attached)
3. **Widow's Peak**: Dominant (**W** = peak); Recessive (**w** = straight hairline)
4. **Hitchhiker's Thumb**: Dominant (**H** = straight); Recessive (**h** = bends back 90°)

### Data Collection

Determine your own phenotype and possible genotype. (If you have the dominant phenotype, you could be homozygous dominant OR heterozygous, so write **T_**).

<!-- lab:data-table rows=5 title="My Genetic Profile" -->
| Trait | My Phenotype | My Possible Genotype(s) |
|---|---|---|
| Tongue Rolling | {fill:text} | {fill:text} |
| Earlobes | {fill:text} | {fill:text} |
| Widow's Peak | {fill:text} | {fill:text} |
| Hitchhiker's Thumb | {fill:text} | {fill:text} |
<!-- /lab:data-table -->

---

## Part 5: Pedigree Analysis

> **Learning Goal:** Interpret family trees to determine inheritance patterns.

A **pedigree** is a chart that tracks a trait through a family.

- **Square** = Male
- **Circle** = Female
- **Shaded** = Affected (has the trait)
- **Unshaded** = Unaffected

### Scenario: Cystic Fibrosis (Autosomal Recessive)

Look at the following description of a family.

1. **Grandparents**: Grandpa (unaffected) and Grandma (unaffected) have a son named Bob (affected with Cystic Fibrosis).
2. **Parents**: Bob marries Sue (unaffected, no family history). They have two kids.
3. **Grandchildren**: Both kids are unaffected.

<!-- lab:reflection -->
**1. Draw this pedigree on a piece of paper.**

**2. What must be the genotype of Grandpa and Grandma? (Use F/f)**
{fill:text}

**3. Why are Grandpa and Grandma called "carriers"?**
{fill:textarea rows=2}

**4. What is Bob's genotype?**
{fill:text}

**5. Assuming Sue is homozygous dominant (FF), what is the genotype of their children?**
{fill:text}
<!-- /lab:reflection -->

---

## Part 6: Sex-Linked Traits

> **Learning Goal:** Understand traits linked to the X chromosome.

Genes on the X chromosome show a unique inheritance pattern. Males (**XY**) have only one X, so they express *whatever* allele is on it, even if recessive. Females (**XX**) can be carriers.

### Scenario: Color Blindness (X-linked Recessive)

- **Xᴮ** = Normal vision
- **Xᵇ** = Color blind

**Problem:** A **carrier female (XᴮXᵇ)** has children with a **normal male (XᴮY)**.

1. Set up the square:

```
       Xᴮ      Xᵇ
     ________________
 Xᴮ |       |        |
    |_______|________|
 Y  |       |        |
    |_______|________|
```

<!-- lab:reflection -->
**1. What is the probability of having a color-blind DAUGHTER?**
{fill:text}

**2. What is the probability of having a color-blind SON?**
{fill:text}

**3. Why represents the genotype of a carrier female?**
{fill:text}

**4. Why are men much more likely to be color blind than women?**
{fill:textarea rows=2}
<!-- /lab:reflection -->

---

## Conclusion

<!-- lab:reflection -->
**1. Explain the Law of Segregation in your own words.**
{fill:textarea rows=2}

**2. If an individual has a dominant phenotype, how could you use a "test cross" to determine if they are homozygous dominant (AA) or heterozygous (Aa)?**
{fill:textarea rows=3}

**3. How does independent assortment contribute to genetic variation?**
{fill:textarea rows=2}
<!-- /lab:reflection -->

---
*Lab created for BIOL-8: Human Biology*
