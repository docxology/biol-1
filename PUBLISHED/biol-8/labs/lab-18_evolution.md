# Lab 18: Evolution — Tragedy of the Commons and Game Theory (Fishing Simulation)

**BIOL-8: Human Biology** | College of the Redwoods, Del Norte Campus

**Name:** {fill:text} **Date:** {fill:text} **Group:** {fill:text}

---

## Purpose

You will work in a **group** to fish a **shared stock** of four kinds of fish over **three seasons.**

The activity connects **evolution and ecology** to **human behavior** in two ways:

- **Tragedy of the commons** — a shared resource can be depleted when many people pursue short-term private gain.
- **Game theory** — your payoff depends on others’ choices; **repeated** seasons change what looks like a good strategy.

After each season, fish that were **not** caught can **reproduce** using a fixed rule. The pool can **recover** or **collapse**, depending on what the group harvests.

---

## Learning objectives

By the end of this lab, you will be able to:

- **Explain** the tragedy of the commons in your own words and relate it to a **shared** fish pool your group managed.
- **Describe** how **rotating** who fishes each season and **rising prices** can change incentives from one round to the next.
- **Apply** the reproduction rule to update population sizes **per species** after a season.
- **Connect** the simulation to **game theory** terms where appropriate: strategy, payoff, cooperation vs. short-term gain, and effects of **repeated** interaction across seasons.
- **Compare** the **four species** by value: gold vs. silver and large vs. small.

---

## Background

### Tragedy of the commons

When a **resource** (pasture, fishery, clean air) is **open to many users** and no one person pays the full **future** cost of overuse, each user can be tempted to take as much as possible **now**. If everyone does that, the **shared stock** shrinks and may **collapse**—even though **no one** wanted that outcome. **Rules**, **quotas**, **catch limits**, and **community agreements** exist partly to avoid that outcome. This lab is a **toy** version of that tension.

### Game theory in one paragraph

**Game theory** models choices when your outcome depends on **others’** choices. In a **repeated** setting (here, **three seasons**), what pays off in season 1 can differ from what pays off after others respond in seasons 2 and 3. You may see **defection** (take a lot) vs. **cooperation** (leave fish for the group and the future) or a mix, depending on your group’s **norms** and the **incentives** your instructor set.

### The four species and value (relative prices)

Relative value (highest to lowest in this model):

| Species | Value in the model |
|--------|------------------------------------|
| **Large goldfish** | **Highest** value per fish (gold and large) |
| **Small goldfish** | High, but **less** than large gold (still gold) |
| **Large silverfish** | **Less** than either gold (silver), but **large** > small for silver |
| **Small silverfish** | **Lowest** value per fish |

**Gold** types are worth more than **silver** types. **Large** types are worth more than **small** types, within the same “metal” group.

**Prices and seasons:** The **price per fish** (what your group “earns” for each type caught) **rises in season 2 and again in season 3** relative to the previous season, so the **temptation** to harvest heavily can **increase** over time unless your group’s strategy accounts for the **reproduction** step.

### Reproduction rule (after each season, before the next)

Work **separately for each of the four species:**

1. Count how many fish of that species were **not** caught (the fish **left in the pool** after that season’s harvest). Call this **N** (a whole number).
2. For that species, the pool **gains** new fish. **Divide N by 2 and round down** to a whole number (in math this is the *floor* of N/2). That number is how many **new** fish of that species you **add**.  
   - Example: N = 5 → 5 / 2 = 2.5 → **2** new fish (round down). New total = 5 + 2 = **7** before the next season.
3. The **caught** fish are **removed** from the pool. They do **not** count toward reproduction in this model.

If your instructor uses a **different** reproduction rule, **follow their version**.

### Connection to “evolution” in BIOL-8

**Evolution** is not only long-term **genetic** change. Biologists also study how **ecological and social** conditions **select** for behaviors, norms, and structures (e.g. cooperation, punishment of cheaters) that affect who survives and **reproduces**—including in **H. sapiens**. This lab is a **classroom analogy**: no real evolution in the fish, but real discussion about **incentives**, **group outcomes**, and **sustainability**—concepts that sit next to **natural selection** in a broader life-science view.

---

## Materials (check with your instructor)

- **Shared pool** of countable units for four “species” (e.g. colored chips, small cards, or tallies) — **large gold**, **small gold**, **large silver**, **small silver**  
- A way to record **start**, **catch**, **left**, **reproduction add**, and **end** counts **per species, per season**  
- **Price list** for each **species** in **each season** (instructor or board)  
- This handout and writing tools  

---

## Procedure

### Before season 1

1. **Form groups** and write **all members’ names** in the roster below. You will use **three fishing seasons.**
2. For **each season,** **one** group member is the **fisher** for that season (someone who was not the fisher the previous time). **Rotate** so **three different people** fish in seasons 1–3 (if the group has fewer than three people, your instructor will say how to handle rotation).
3. Copy the **starting population** for each **species** from the instructor (or the board) into **Table 1** under **Start (Season 1).**
4. Copy the **price per fish** for **each species in season 1** into **Table 2** (or record “see board” and keep your own clear notes).

### Each season (repeat for seasons 1, 2, and 3)

1. The **fisher** for that season “catches” by **taking** units from the pool as allowed by the rules your instructor gives (e.g. **maximum** number of fish, or a **time** limit, or a **fixed** haul). Record **only** the **number caught per species** in **Table 1** in the **Catch** row for that season.
2. **After** the catch, compute **left** in the pool: **Start − catch** (per species) for that season. Enter under **Left after catch.**
3. **Reproduction:** For **each** species, compute **add** = (**Left after catch**) / 2, **rounded down** to a whole number. New count before the next season = **Left after catch** + **add**. Enter under **Repro add** and **End (after repro).** The **End** row is the **Start** for the next season.
4. **Earnings for this season:** For each species, **(catch) × (price for that species in this season).** Sum to get **group earnings** for the season. Use **Table 2**; your instructor will give **season 2 and season 3** prices (higher than before).
5. The **next** group member **fishes** the following season, starting from the new **Start** row.

### After season 3

- Total **cumulative** earnings if your instructor requests it.  
- Complete **Table 1** and **Table 2**, then the **Analysis** and **Conclusion** sections.

---

<div style="page-break-before: always;"></div>

## Data

**Abbreviations:** LG = large gold, SG = small gold, LS = large silver, SS = small silver.

### Group roster (fill in before Season 1)

<!-- lab:data-table rows=4 title="Group roster" -->
| Role | Name |
|------|------|
| Fisher — Season 1 | {fill:text} |
| Fisher — Season 2 | {fill:text} |
| Fisher — Season 3 | {fill:text} |
| Other group members (if any) | {fill:text} |
<!-- /lab:data-table -->

### Table 1 — Population and catch (all three seasons)

**Starting populations (from instructor)** go in the **Start — Season 1** row below.

<!-- lab:data-table rows=5 title="Table 1 — Season 1 population and catch" -->
| | Large gold (LG) | Small gold (SG) | Large silver (LS) | Small silver (SS) |
|--|-----------------|-----------------|--------------------|--------------------|
| **Start — Season 1** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **Catch — Season 1** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **Left after catch — S1** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **Repro add — S1** (left / 2, round down) | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **End after repro — S1** (= left + add) | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
<!-- /lab:data-table -->

**Season 2** — *Fisher (name):* {fill:text}

<!-- lab:data-table rows=5 title="Table 1 (continued) — Season 2" -->
| | LG | SG | LS | SS |
|--|----|----|----|----|
| **Start** (= end S1) | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **Catch** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **Left after catch** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **Repro add** (left / 2, round down) | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **End after repro** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
<!-- /lab:data-table -->

**Season 3** — *Fisher (name):* {fill:text}

<!-- lab:data-table rows=5 title="Table 1 (continued) — Season 3" -->
| | LG | SG | LS | SS |
|--|----|----|----|----|
| **Start** (= end S2) | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **Catch** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **Left after catch** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **Repro add** (left / 2, round down) | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
| **End after repro** | {fill:text} | {fill:text} | {fill:text} | {fill:text} |
<!-- /lab:data-table -->

### Table 2 — Prices by season, then earnings

Copy **price per fish** from the instructor. **Earnings** for a season = sum over species of (catch that season) × (price that season for that species).

<!-- lab:data-table rows=4 title="Table 2 — Price per fish by season" -->
| Species | Price — Season 1 | Price — Season 2 | Price — Season 3 |
|--------|------------------|-----------------|-----------------|
| LG | {fill:text} | {fill:text} | {fill:text} |
| SG | {fill:text} | {fill:text} | {fill:text} |
| LS | {fill:text} | {fill:text} | {fill:text} |
| SS | {fill:text} | {fill:text} | {fill:text} |
<!-- /lab:data-table -->

<!-- lab:data-table rows=4 title="Table 2 — Earnings by season" -->
| Season | Earnings (show work or subtotal) |
|--------|------------------------------------|
| 1 | {fill:text} |
| 2 | {fill:text} |
| 3 | {fill:text} |
| **Total (all seasons)** | {fill:text} |
<!-- /lab:data-table -->

---

<div style="page-break-before: always;"></div>

## Analysis

Answer in **complete sentences**. Use your **tables** for any question that refers to your group’s numbers.

<!-- lab:reflection -->
**1. Tragedy of the commons.** In two or three sentences, did your group’s pool **trend toward depletion, stability, or recovery** for one or more species? Name **one** choice that made that outcome more likely.

{fill:textarea rows=4}
<!-- /lab:reflection -->

<!-- lab:reflection -->
**2. Evolution of incentives.** **Prices rose** each season. How did that affect what you think the “best” **short-term** move was, versus a **long-term** group goal?

{fill:textarea rows=4}
<!-- /lab:reflection -->

<!-- lab:reflection -->
**3. Game theory.** Name **one** behavior that acted like **cooperation** and **one** that acted like **defection** (or self-interest only), whether or not you used those words during the game.

{fill:textarea rows=4}
<!-- /lab:reflection -->

<!-- lab:reflection -->
**4. Reproduction rule.** For **one** species, show with numbers: **left after catch**, **repro add** (left / 2, **round down**), and **end** after you add. Did the rule ever **increase** the stock enough that your group was glad some fish were **left in the pool**?

{fill:textarea rows=4}
<!-- /lab:reflection -->

---

## Conclusion

<!-- lab:reflection -->
**5. Human biology in one sentence:** Why might a **lecture** on evolution in humans include a **resource** and **incentive** story like this, not only DNA and fossils?

{fill:textarea rows=3}
<!-- /lab:reflection -->

---

*Lab 18 — Evolution. Tragedy of the commons and game theory via a three-season fishing simulation.*
