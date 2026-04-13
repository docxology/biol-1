# Lab 14: How Populations Evolve (Module 13)

**Name:** {fill:text} **Date:** {fill:text}

## Overview

Today you run a **paper simulation** of one imaginary beetle population across **three generations of story time**. You will track **allele frequencies**, watch **random catastrophe** reshuffle them (drift), then watch **non-random survival** (selection) change the distribution. The point is not algebra tricks—it is to feel **when chance matters** and **when the environment steers evolution**.

## Learning Objectives

By the end of this lab, you should be able to:

1. Calculate allele frequency from genotype counts in a diploid population.
2. Explain how a **bottleneck** can change allele frequencies **without** selection.
3. Classify **directional / stabilizing / disruptive** selection from a before-and-after phenotype distribution.
4. Use Hardy–Weinberg expectations as a **null model** (“what if nothing evolutionary happened?”).

## Materials Needed

- Pencil or pen
- This worksheet
- Calculator (optional)

---

## Warm-up

<!-- lab:reflection -->
**W1.** In one sentence, what is a **population** in biology (the evolutionary meaning—not just “many animals in one place”)?  
{fill:textarea rows=2}

**W2. Gene vs alleles:** This lab follows one gene with two versions, **R** and **r**. In one sentence, what does it mean to say **R** and **r** are two **alleles**?  
{fill:textarea rows=2}

**W3. Allele frequency:** In one sentence, what does **allele frequency** measure—you count copies of an allele, whole individuals, or something else?  
{fill:text}

**W4. Diploid count:** One beetle has genotype **Rr**. How many **r** alleles does that one beetle carry? (enter a number)  
{fill:text}
<!-- /lab:reflection -->

---

## Part 1: Lakeview Beetles — Baseline (Generation 0)

*Gene **R** controls spot brightness: **RR** = bright, **Rr** = mottled, **rr** = dull. Population is at Hardy–Weinberg expectations for this generation.*

In **Generation 0**, scientists genotype **200** beetles:

| Genotype | Number of individuals |
|---|---|
| RR | 50 |
| Rr | 100 |
| rr | 50 |

<!-- lab:reflection -->
**1. Count alleles (show work in the margin of your paper if needed).**

- Total **R** alleles in the population: {fill:text}  
- Total **r** alleles: {fill:text}  
- Total alleles (diploid population): {fill:text}

**2. Allele frequencies:**  
- Frequency of **R** (call it *p*): {fill:text}  
- Frequency of **r** (*q*): {fill:text}  
- Check: does *p* + *q* = 1? {fill:text}

**3. Null expectation:** If mating is random and nothing evolutionary happens, predict approximate genotype frequencies using *p*², 2*pq*, and *q*² (you may round to two decimals).  
- Expected **RR**: {fill:text} **Rr**: {fill:text} **rr**: {fill:text}

**4. Quick check:** Do the observed counts (50 / 100 / 50) match your expectations **exactly**? **Yes / No.** (Real populations often deviate—your job is to notice.)  
{fill:textarea rows=2}
<!-- /lab:reflection -->

---

## Part 2: The Dam Break — Bottleneck (Generation 1)

*A flash flood strands beetles on a tiny mud island. Only **20** beetles survive—**randomly** with respect to genotype (no selection yet). Survivors:*

| Genotype among survivors | Count |
|---|---|
| RR | 4 |
| Rr | 8 |
| rr | 8 |

<!-- lab:reflection -->
**5. Prediction first:** Before you calculate, did you expect *p* to stay exactly **0.5**? **Yes / No.** One sentence why drift should or shouldn’t matter here:  
{fill:textarea rows=2}

**6. Calculate new allele frequencies among **survivors only** (20 individuals = 40 alleles).**  
- Total **R** alleles: {fill:text}  
- Total **r** alleles: {fill:text}  
- New *p*: {fill:text} New *q*: {fill:text}

**7. Interpret:** Did the allele frequency change **because birds preferred bright beetles**? **Yes / No.** What **mechanism** caused the change in this part of the story?  
{fill:textarea rows=3}
<!-- /lab:reflection -->

---

<div style="page-break-after: always;"></div>

## Part 3: Bird Arrival — Selection (Generation 2)

*Birds colonize the mud island. The visual background is patchy: sometimes bright rock, sometimes deep shadow. **Mottled** beetles are caught most often because they match neither extreme. **Bright** and **dull** extremes both survive better than the middle. After one round of reproduction, the **adult** phenotype distribution has thinned at the center.*

<!-- lab:reflection -->
**8. Classify the mode of natural selection acting on spot brightness.**  
Circle one: **Directional / Stabilizing / Disruptive** — defend in two sentences (what happens to the **middle** of the distribution vs the **extremes**?).  
{fill:textarea rows=4}

**9. Mechanism check:** Which of the five microevolutionary mechanisms **dominates** this bird episode? (mutation / gene flow / drift / non-random mating / natural selection)  
{fill:text}

**10. Could **gene flow** later undo this local adaptation?** Describe a realistic scenario in 2–3 sentences (e.g., bright beetles fly in from the mainland).  
{fill:textarea rows=4}
<!-- /lab:reflection -->

---

## Part 4: Hardy–Weinberg as a Foil

*Hardy–Weinberg is the “boring universe” where allele frequencies never change. Real populations are more interesting.*

<!-- lab:reflection -->
**11. Name two assumptions of Hardy–Weinberg equilibrium** (any two standard ones):  
1. {fill:text}  
2. {fill:text}

**12. In this simulation, which assumptions were clearly violated in Part 2? In Part 3?** (short phrases)  
- Part 2: {fill:text}  
- Part 3: {fill:text}

**13. Independent practice:** A gene has dominant allele frequency *p* = 0.2. Find *q*, then **aa** frequency, then **Aa** heterozygote frequency.  
- *q* = {fill:text}  
- Freq(**aa**) = *q*² = {fill:text}  
- Freq(**Aa**) = 2*pq* = {fill:text}

**14. Big picture (3 sentences):** Why is it useful to compare **real** genotype frequencies to **Hardy–Weinberg expectations** instead of memorizing “equilibrium” as magic?  
{fill:textarea rows=4}
<!-- /lab:reflection -->
