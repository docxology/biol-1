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
- **Describe** how **rotating** who fishes each season and **rising point values** (each season pays more per fish) can change incentives from one round to the next.
- **Apply** the reproduction rule to update population sizes **per species** after a season.
- **Connect** the simulation to **game theory** terms where appropriate: strategy, payoff, cooperation vs. short-term gain, and effects of **repeated** interaction across seasons.
- **Compare** the **four species** by value: gold vs. silver and large vs. small.

---

## Background

### Tragedy of the commons

When a **resource** (pasture, fishery, clean air) is **open to many users** and no one person pays the full **future** cost of overuse, each user can be tempted to take as much as possible **now**. If everyone does that, the **shared stock** shrinks and may **collapse**—even though **no one** wanted that outcome. **Rules**, **quotas**, **catch limits**, and **community agreements** exist partly to avoid that outcome. This lab is a **toy** version of that tension.

### Game theory in one paragraph

**Game theory** models choices when your outcome depends on **others’** choices. In a **repeated** setting (here, **three seasons**), what pays off in season 1 can differ from what pays off after others respond in seasons 2 and 3. You may see **defection** (take a lot) vs. **cooperation** (leave fish for the group and the future) or a mix, depending on your group’s **norms** and the **rising point values** in the schedule.

### The four species and value (relative prices)

Relative value (highest to lowest in this model):

| Species | Value in the model |
|--------|------------------------------------|
| **Large goldfish** | **Highest** value per fish (gold and large) |
| **Small goldfish** | High, but **less** than large gold (still gold) |
| **Large silverfish** | **Less** than either gold (silver), but **large** > small for silver |
| **Small silverfish** | **Lowest** value per fish |

**Gold** types are worth more than **silver** types. **Large** types are worth more than **small** types, within the same “metal” group.

**Prices and seasons:** Earnings are in **class points** per fish, using the **fixed schedule** in the **Data** section below (**Table 2**), unless your instructor posts a different table. **Every** species earns **more points** in **season 2** than in **season 1**, and more again in **season 3**—so the pull to overharvest can grow each round if your group does not protect the stock.

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

## Materials

- **Shared pool** of countable units for four species (e.g. colored chips, small cards, or tallies) — **large gold**, **small gold**, **large silver**, **small silver**  
- A way to record **start**, **catch**, **left**, **reproduction add**, and **end** counts **per species, per season**  
- The **point schedule** printed in this handout (Table 2) — *your instructor may substitute; use their values if so*  
- This handout and writing tools  

---

## Procedure

### Before season 1

1. **Form groups** and write **all members’ names** in the roster below. You will use **three fishing seasons.**
2. For **each season,** **one** group member is the **fisher** for that season (someone who was not the fisher the previous time). **Rotate** so **three different people** fish in seasons 1–3 (if the group has fewer than three people, your instructor will say how to handle rotation).
3. Copy the **starting population** for each **species** from the instructor (or the board) into **Table 1** under **Start (Season 1).**
4. Use the **price schedule (points per fish)** printed in **Table 2** below for all earnings, **unless** your instructor gives a different table—then use theirs for every season.

### Each season (repeat for seasons 1, 2, and 3)

1. The **fisher** for that season “catches” by **taking** units from the pool as allowed by the rules your instructor gives (e.g. **maximum** number of fish, or a **time** limit, or a **fixed** haul). Record **only** the **number caught per species** in **Table 1** in the **Catch** row for that season.
2. **After** the catch, compute **left** in the pool: **Start − catch** (per species) for that season. Enter under **Left after catch.**
3. **Reproduction:** For **each** species, compute **add** = (**Left after catch**) / 2, **rounded down** to a whole number. New count before the next season = **Left after catch** + **add**. Enter under **Repro add** and **End (after repro).** The **End** row is the **Start** for the next season.
4. **Earnings for this season:** For each species, **(catch) × (points for that species in this season)** from the **Table 2** price grid. Add the four products to get **group points** for the season. Do the same for seasons 2 and 3 using the **points columns** for that season in the same table.
5. The **next** group member **fishes** the following season, starting from the new **Start** row.

### After season 3

- Total **cumulative** earnings if your instructor requests it.  
- Complete **Table 1** and **Table 2**, then the **Analysis** and **Conclusion** sections.

---

<div style="page-break-before: always;"></div>

## Data

**Abbreviations:** LG = large gold, SG = small gold, LS = large silver, SS = small silver.

*Show at least one season’s **earnings** as a sum of **(catch × points)** for each species (in **Table 2** or the work space below the price table).*

### Group roster (fill in before Season 1)

<h3>Group roster</h3>
<table class="lab-table">
<thead>
<tr><th scope="col">Role</th><th scope="col">Name</th></tr>
</thead>
<tbody>
<tr><th scope="row">Fisher — Season 1</th><td>{fill:text}</td></tr>
<tr><th scope="row">Fisher — Season 2</th><td>{fill:text}</td></tr>
<tr><th scope="row">Fisher — Season 3</th><td>{fill:text}</td></tr>
<tr><th scope="row">Other group members (if any)</th><td>{fill:text}</td></tr>
</tbody>
</table>

### Table 1 — Population and catch (all three seasons)

**Starting populations (from instructor)** go in the **Start — Season 1** row below.

<h3>Table 1 — Season 1</h3>
<table class="lab-table">
<thead>
<tr>
<th scope="col"></th>
<th scope="col">Large gold (LG)</th>
<th scope="col">Small gold (SG)</th>
<th scope="col">Large silver (LS)</th>
<th scope="col">Small silver (SS)</th>
</tr>
</thead>
<tbody>
<tr><th scope="row">Start — Season 1</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">Catch — Season 1</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">Left after catch — S1</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">Repro add — S1 (left / 2, round down)</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">End after repro — S1 (= left + add)</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
</tbody>
</table>

**Season 2** — *Fisher (name):* {fill:text}

<h3>Table 1 — Season 2</h3>
<table class="lab-table">
<thead>
<tr>
<th scope="col"></th>
<th scope="col">LG</th>
<th scope="col">SG</th>
<th scope="col">LS</th>
<th scope="col">SS</th>
</tr>
</thead>
<tbody>
<tr><th scope="row">Start (= end S1)</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">Catch</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">Left after catch</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">Repro add (left / 2, round down)</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">End after repro</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
</tbody>
</table>

**Season 3** — *Fisher (name):* {fill:text}

<h3>Table 1 — Season 3</h3>
<table class="lab-table">
<thead>
<tr>
<th scope="col"></th>
<th scope="col">LG</th>
<th scope="col">SG</th>
<th scope="col">LS</th>
<th scope="col">SS</th>
</tr>
</thead>
<tbody>
<tr><th scope="row">Start (= end S2)</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">Catch</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">Left after catch</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">Repro add (left / 2, round down)</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
<tr><th scope="row">End after repro</th><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td><td>{fill:text}</td></tr>
</tbody>
</table>

### Table 2 — Price schedule (class default) and earnings

**Points per fish caught** — use these values for **earnings** unless your instructor replaces them. **Gold** rows earn more than **silver**; **large** more than **small**; each **season** pays more per fish than the last.

<table class="lab-table">
<thead>
<tr>
<th scope="col">Species</th>
<th scope="col">Points — Season 1</th>
<th scope="col">Points — Season 2</th>
<th scope="col">Points — Season 3</th>
</tr>
</thead>
<tbody>
<tr><th scope="row"><strong>LG</strong> (large gold)</th><td>8</td><td>12</td><td>18</td></tr>
<tr><th scope="row"><strong>SG</strong> (small gold)</th><td>4</td><td>6</td><td>9</td></tr>
<tr><th scope="row"><strong>LS</strong> (large silver)</th><td>2</td><td>3</td><td>5</td></tr>
<tr><th scope="row"><strong>SS</strong> (small silver)</th><td>1</td><td>2</td><td>3</td></tr>
</tbody>
</table>

**Earnings** for a season = **sum** over the four species of **(number caught) × (points for that species in that season).**

<!-- lab:reflection -->
**Work space (one season, optional check):** Pick **one** season and write **(catch × points)** for each species, then the **sum** (should match the row you enter in the Earnings table below).  
{fill:textarea rows=4}
<!-- /lab:reflection -->

<h3>Table 2 — Earnings by season (points)</h3>
<table class="lab-table">
<thead>
<tr>
<th scope="col">Season</th>
<th scope="col">Group earnings (show work or subtotal)</th>
</tr>
</thead>
<tbody>
<tr><th scope="row">1</th><td>{fill:text}</td></tr>
<tr><th scope="row">2</th><td>{fill:text}</td></tr>
<tr><th scope="row">3</th><td>{fill:text}</td></tr>
<tr><th scope="row">Total (all seasons)</th><td>{fill:text}</td></tr>
</tbody>
</table>

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
