# Lab 13: Darwin & Evolution (Module 12)

**Name:** {fill:text} **Date:** {fill:text}

## Overview

You are not rehearsing definitions today—you are **playing biologist**. Each part is a **mini scenario**: you will make a **prediction**, watch a **story outcome** (on paper), and then **defend** whether natural selection, evidence, or “common sense” actually fits. Part 3 adds a simple **genetic model** so you can connect **Mendelian ratios** to **allele frequency change** after selection. The thread is simple: evolution is **population-level**, **evidence-based**, and **mechanistic**, not a ladder of “better animals.”

## Learning Objectives

By the end of this lab, you should be able to:

1. Use the **variation → overproduction → differential reproductive success** logic to predict trait change in a changing environment.
2. Use a **Punnett square** for one gene and track how **selection** changes **allele frequencies** in a single generation.
3. Apply the biological meaning of **fitness** to messy, realistic vignettes.
4. Choose which **line of evidence** tests which kind of claim about history and relatedness.
5. Explain why **individuals do not evolve** while **populations** can.

## Materials Needed

- Pencil or pen
- This worksheet
- Calculator (optional, for division)

---

## Part 1: Natural selection in two habitats (Clipperton stick insects)

*Imagine an island with two habitats: **open lava** (dark rock) and **mossy groves** (bright green). A single species of stick insect comes in two heritable color morphs: **charcoal** and **leaf-green**. Insect-eating birds hunt by sight.*

<!-- lab:reflection -->
**1. Before you read the “results,” write a hypothesis.**

**Hypothesis 1 (lava plots):** Over many generations on open lava, do you expect charcoal or leaf-green morphs to become more common? **Circle one:** Charcoal / Leaf-green / No change — then **one sentence why:**  
{fill:textarea rows=2}

**Hypothesis 2 (moss groves):** In bright green moss, do you expect charcoal or leaf-green to become more common? **Circle one:** Charcoal / Leaf-green / No change — **one sentence why:**  
{fill:textarea rows=2}

**2. “Field notes” (given):** After 30 generations, lava plots are ~85% charcoal; moss groves are ~80% leaf-green. Bird stomach contents show they capture what stands out against the background.

**Match mechanism to story:** What is the **selective agent**? What is being **selected** (which phenotypes leave more offspring)?  

- Selective agent: {fill:text}  
- What increases in each habitat (one short phrase each):  
  - On lava: {fill:text}  
  - In moss: {fill:text}

**3. Revision check:** Did your hypotheses match the outcomes? If not, what environmental detail would you add to your model next time?  
{fill:textarea rows=3}
<!-- /lab:reflection -->

---

## Part 2: What “fitness” means (short scenarios)

*Evolutionary fitness is **offspring that survive to reproduce**, not bench press scores.*

<!-- lab:reflection -->
**4. One-sentence definition of evolutionary fitness (your words):**  
{fill:textarea rows=2}

**5. “Tournament bracket” — who has higher fitness here?** Write **higher** or **lower** for each animal **in evolutionary terms**.

| Competitor story | Fitness (higher / lower) |
|---|---|
| Bull moose A: huge antlers, wins fights, **0 calves** | {fill:text} |
| Bull moose B: smaller antlers, avoids fights, **3 calves survive to yearling** | {fill:text} |
| Salmon that dies after spawning but fertilizes **thousands of eggs** | {fill:text} |
| Long-lived turtle that **never** successfully reproduces | {fill:text} |

**6. Puzzle:** A new antibiotic saves infected bacteria **before** they reproduce (they survive but never divide). Does this antibiotic **increase bacterial fitness** in evolutionary terms? Explain.  
{fill:textarea rows=3}
<!-- /lab:reflection -->

---

## Part 3: Genetics of color — Punnett square and one generation on lava

*We model the same species with **one gene** and **two alleles**, with **complete dominance**:*

- **C** = dominant allele → **charcoal** phenotype (`CC` or `Cc`)  
- **c** = recessive allele → **leaf-green** phenotype only when homozygous **`cc`**

Two heterozygotes mate: **`Cc` × `Cc`**.

<!-- lab:reflection -->
**7. Write the phenotype for each genotype.**

| Genotype | Phenotype (charcoal or leaf-green) |
|---|---|
| `CC` | {fill:text} |
| `Cc` | {fill:text} |
| `cc` | {fill:text} |

**8. Complete the Punnett square** for `Cc` × `Cc`. Each parent makes gametes **C** and **c**.

| | **C** | **c** |
|---|---|---|
| **C** | {fill:text} | {fill:text} |
| **c** | {fill:text} | {fill:text} |

**9. From the square, give the expected zygote ratios** (use form `1 ___ : 2 ___ : 1 ___`).  
{fill:text}

**10.** Expected *phenotype* ratio among those zygotes (charcoal vs leaf-green):  
{fill:text}

**11. One generation on lava (differential survival).** Imagine **400** new zygotes in the exact proportions above: **100 `CC`, 200 `Cc`, 100 `cc`**. On open lava, bright green stands out to birds. Use these **relative survival** values (viability before reproduction):

- `w_CC = 1.0` `w_Cc = 1.0` `w_cc = 0.25`

**Prediction:** Before you calculate, do you expect the frequency of the **`c`** allele among survivors to **go up**, **go down**, or **stay the same**? One sentence why.  
{fill:textarea rows=2}

**12. Count survivors** (multiply number of each genotype by its `w`):

| Genotype | Number before selection | × `w` | Survivors (individuals) |
|---|---|---|
| `CC` | 100 | × 1.0 | {fill:text} |
| `Cc` | 200 | × 1.0 | {fill:text} |
| `cc` | 100 | × 0.25 | {fill:text} |
| **Total** | 400 | — | **{fill:text}** |

**13. Allele counting among survivors only.** Each diploid individual carries **2** alleles.

- Total **C** alleles in survivors: {fill:text} *(Hint: `CC` contributes 2 per individual, `Cc` contributes 1.)*  
- Total **c** alleles in survivors: {fill:text} *(Hint: `Cc` contributes 1 per individual, `cc` contributes 2.)*  
- Total alleles = 2 × (number of survivors): {fill:text}

**14. Frequencies after selection (among survivors):**

- Frequency of **c** (call it \(q_{\text{after}}\)): {fill:text} *( = total c alleles ÷ total alleles)*  
- Frequency of **C** (\(p_{\text{after}}\)): {fill:text}

**15. Compare to the starting zygote pool** (before selection): there were **400 C** and **400 c** alleles in 400 individuals, so \(p = q = 0.5\). Did \(q\) **increase** or **decrease** after one generation on lava? Does that match Part 1’s lava story?  
{fill:textarea rows=3}

**16. (Optional stretch)** On **moss**, suppose leaf-green blends in best. Sketch a pattern of relative survival (`w`) across genotypes that would favor **`cc`** *without* writing a full calculation.  
{fill:textarea rows=2}
<!-- /lab:reflection -->

---

<div style="page-break-after: always;"></div>

## Part 4: Matching scientific claims to the strongest line of evidence

**Evidence menu (pick one letter per row):**  
**A** **Fossils & stratigraphy** — order of forms in rock layers; transitional morphology in time.  
**B** **Homologous structures (comparative anatomy)** — same underlying plan, different function (e.g., limb bones).  
**C** **Biogeography** — where species live relative to geology and dispersal history.  
**D** **Molecular sequences (DNA/proteins)** — similarity and branching when anatomy is misleading.

<!-- lab:reflection -->
**17. Which line of evidence best addresses each claim?** Write **A**, **B**, **C**, or **D**.

| Claim | Best evidence |
|---|---|
| “Whales look nothing like hippos today—yet detailed **skeletal homologies** (and fossils) link whales to even-toed ungulates.” *(Which line is the **primary** match for **unexpected anatomical correspondences**?)* | {fill:text} |
| “Why are **marsupials** so concentrated in Australia compared with placental mammals on other continents?” | {fill:text} |
| “Can we see **fish-to-tetrapod** intermediates and their **order in the fossil record**?” | {fill:text} |
| “When **convergent evolution** makes two groups look similar, which data often resolve **true branching order**?” | {fill:text} |

**18. Convergence vs homology (bat vs bird).** Bat wings and bird wings are both used for flight but evolved from different forelimb histories.

**a)** Are those wings **homologous as wings** in the everyday sense of “same structure, same recent origin”? **Yes / No** — one sentence.  
{fill:textarea rows=2}

**b)** What would you compare next to decide **deep ancestry** vs **convergence** (name at least two: e.g., bone-by-bone forelimb, fossils, genes)?  
{fill:textarea rows=3}

**19. Burrowing look-alikes.** Two distantly related lineages evolve **similar-looking** cylindrical bodies for burrowing.

**a)** Is surface similarity alone strong evidence of **recent** common ancestry? **Yes / No** — why?  
{fill:textarea rows=2}

**b)** What evidence types from the A–D menu would you combine to test history?  
{fill:textarea rows=2}
<!-- /lab:reflection -->

---

## Part 5: Individuals vs populations (inheritance and evolution)

*You already know DNA replication and the universal code (Module 07). Now stress-test “population thinking.”*

<!-- lab:reflection -->
**20. Thought experiment — “Super-Soldier Serum” (fiction):** A person’s muscles triple in size after an injection, but **gamete DNA is unchanged**.

**Prediction:** Can their children inherit bigger muscles **because of the injection**? **Yes / No.**  
**Explain using “individual vs population” and heritability:**  
{fill:textarea rows=4}

**21. Fix the broken claims:**

| Claim | True / False | Fix in one sentence |
|---|---|---|
| “That bird evolved a sharper beak during its life to crack nuts.” | {fill:text} | {fill:text} |
| “The population’s average beak depth increased across generations because shallow-beaked birds starved during a drought.” | {fill:text} | {fill:text} |

**22. Synthesis (3–4 sentences):** Why does the **genetic code’s universality** make a **single tree of life** plausible?  
{fill:textarea rows=5}
<!-- /lab:reflection -->
