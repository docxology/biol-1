# Lab 11: Inheritance — Genetics Problems

## Overview

Gregor Mendel's experiments with pea plants revealed that inheritance is not a "blending" of traits, but rather the passing down of discrete physical units (which we now call genes). Mendelian genetics allows us to predict the probability of traits in offspring.

In this lab, you will apply Mendel’s Laws (Segregation and Independent Assortment) to solve genetics problems. You will track inheritance patterns from simple complete dominance to more complex real-world scenarios like codominance, incomplete dominance, and sex-linked traits, concluding with an analysis of human pedigrees.

## Learning Objectives

By the end of this lab, you will be able to:

1. Define correctly: Allele, Genotype, Phenotype, Homozygous, Heterozygous, Dominant, and Recessive.
2. Use Punnett squares to predict genotypic and phenotypic ratios for monohybrid and dihybrid crosses.
3. Solve complex probability problems involving Non-Mendelian inheritance (Incomplete Dominance, Codominance/Blood Types, Sex-Linked traits).
4. Analyze a multi-generational pedigree to deduce whether a specific human trait is Autosomal or Sex-Linked, Dominant or Recessive.

## Materials

* Review Packet (this document)
* Scratch paper for working out large Punnett squares
* Calculator (optional, for probabilities)

---

## Part 1: Simple Complete Dominance (Monohybrid Crosses)

In complete dominance, the dominant allele strictly masks the recessive allele in the heterozygote.

**Trait:** In pea plants, Purple flowers ($P$) are dominant to White flowers ($p$).

**Problem 1A:** A homozygous dominant purple plant is crossed with a homozygous recessive white plant.

* **Parents:** $PP \times pp$
* Set up a Punnett square.

<!-- lab:reflection -->
**1. What are the genotypes and phenotypes of the resulting F₁ generation?**

{fill:textarea rows=3}
<!-- /lab:reflection -->

**Problem 1B:** Two of the F₁ generation plants from above are crossed.

* **Parents:** $Pp \times Pp$
* Set up a Punnett square.

<!-- lab:reflection -->
**2. What is the expected *Genotypic* Ratio of the F₂ offspring? (Format: PP : Pp : pp)**

{fill:text}

**3. What is the expected *Phenotypic* Ratio of the F₂ offspring? (Format: Purple : White)**

{fill:text}
<!-- /lab:reflection -->

---

## Part 2: Independent Assortment (Dihybrid Crosses)

When tracking two traits at once on different chromosomes, the alleles assort independently into gametes.

**Traits:** In guinea pigs, Black hair ($B$) is dominant to Brown hair ($b$). Short hair ($S$) is dominant to Long hair ($s$).

**Problem 2:** Two guinea pigs that are heterozygous for *both* traits are mated.

* **Parents:** $BbSs \times BbSs$

1. **Determine Gametes:** Use the FOIL method (First, Outer, Inner, Last) to find the four possible gametes for each parent. (Gametes should have one $B/b$ allele and one $S/s$ allele).
    * *Gametes:* $BS$, $Bs$, $bS$, $bs$
2. **Punnett Square:** Set up a 16-square grid on your scratch paper. Put the male gametes on top and the female gametes on the side. Fill it in.

<!-- lab:reflection -->
**4. Out of 16 possible offspring, how many are expected to have the following phenotypes?**

* Black and Short: {fill:text}
* Black and Long: {fill:text}
* Brown and Short: {fill:text}
* Brown and Long: {fill:text}
<!-- /lab:reflection -->

---

## Part 3: Non-Mendelian Inheritance

The real world is rarely as simple as Mendel's peas.

### 3A. Incomplete Dominance

The heterozygote shows a *blended* intermediate phenotype.

**Trait:** In snapdragon flowers, Red ($C^R$) and White ($C^W$) exhibit incomplete dominance. The heterozygote ($C^R C^W$) is Pink.
**Problem 3A:** Cross a Pink snapdragon with a White snapdragon. ($C^R C^W \times C^W C^W$)

<!-- lab:reflection -->
**5. What percentage of the offspring will be Pink? What percentage will be Red?**

{fill:textarea rows=2}
<!-- /lab:reflection -->

### 3B. Codominance and Multiple Alleles (Blood Typing)

Human ABO blood type is determined by three possible alleles: $I^A$ (Type A), $I^B$ (Type B), and $i$ (Type O, recessive). $I^A$ and $I^B$ are codominant (creating Type AB blood if both are present).

**Problem 3B:** A mother has Type A blood (but her father was Type O, meaning she must be a carrier: genotype $I^A i$). The father has Type B blood (and his mother was Type O, so he is $I^B i$).

<!-- lab:reflection -->
**6. Set up the Punnett square. What are the possible blood types of their children, and in what probabilities?**

{fill:textarea rows=3}

**7. Can these parents have a child with Type O blood? Explain.**

{fill:textarea rows=2}
<!-- /lab:reflection -->

### 3C. Sex-Linked (X-Linked) Traits

Genes located on the X chromosome show unique inheritance because males ($XY$) only have one copy, while females ($XX$) have two.

**Trait:** Red-Green colorblindness is an X-linked recessive trait ($X^b$). Normal vision is dominant ($X^B$).

**Problem 3C:** A colorblind man ($X^b Y$) marries a woman with normal vision who is a carrier ($X^B X^b$).

<!-- lab:reflection -->
**8. What is the probability that their sons will be colorblind?**

{fill:text}

**9. What is the probability that their daughters will be colorblind?**

{fill:text}

**10. Why are X-linked recessive traits much more common in biological males than females?**

{fill:textarea rows=3}
<!-- /lab:reflection -->

---

## Part 4: Pedigree Analysis

Pedigrees are family trees that track a specific trait across generations.

* **Squares** = Males
* **Circles** = Females
* **Shaded** = Has the trait being tracked
* **Unshaded** = Does NOT have the trait

**Analyze a hypothetical pedigree provided by your instructor or drawn on the board.** The pedigree shows a disease trait. It appears in Generation I, skips Generation II (where all children are unaffected), but suddenly reappears in Generation III. In Generation II, two unaffected parents have an affected daughter.

<!-- lab:reflection -->
**11. Is this trait Dominant or Recessive? How do you know?**

{fill:textarea rows=3}

**12. Is this trait Autosomal or X-Linked? Justify your answer using the fact that two unaffected parents had an affected *daughter*.** *(Hint: What allele must the father pass to all his daughters?)*

{fill:textarea rows=4}
<!-- /lab:reflection -->

## Conclusion

Genetics is a game of rigorous probability. By understanding the physical mechanism of how homologous chromosomes separate during meiosis, we can accurately predict the likelihood of varied traits, track diseases through family lineages, and understand the genetic basis of human diversity.
