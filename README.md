# Pharma Brand Launch Analytics

**An end-to-end commercial analytics suite for a pharmaceutical brand launch — built on real CMS Medicare Part D data.**

Segmenting 282,123 US anticoagulant prescribers, sizing a salesforce, designing territories, and modeling incentive compensation — the exact workflow a life-sciences commercial analytics team runs before a launch.

---

## The Business Problem

**Corvana Therapeutics** (fictional client) is preparing to launch **Carddil (fluxaban)**, a novel oral factor Xa inhibitor, into the US anticoagulant market — an established, crowded category where Eliquis and Xarelto displaced 60-year incumbent warfarin.

Because the entry is late into a competitive market, success depends entirely on **commercial execution**. The VP of Commercial Operations needs three questions answered:

1. **Whom do we target?** — 282K prescribers exist; a rep costs ~$250K/year. Who is worth a visit?
2. **How do we cover them?** — How many reps, calling on whom, how often, in which territories?
3. **How do we pay them?** — What incentive structure motivates without blowing the budget?

This project answers all three.

---

## Data

| | |
|---|---|
| **Source** | CMS Medicare Part D Prescribers by Provider and Drug (real, public, API) |
| **Scope** | 6 anticoagulants — Eliquis, Xarelto, Warfarin Sodium, Pradaxa, Savaysa, Jantoven |
| **Volume** | 511,302 prescriber–drug rows -> 282,123 unique prescribers |

**Real market layer, simulated commercial layer.** The prescriber and prescribing data is 100% real CMS data. The commercial constructs (territories, rep calls, sales goals, payouts) are **simulated**, because that data is client-confidential at every pharma company — the same way firms build test environments.

**Known limitation:** Part D covers only the 65+ Medicare population. This is acceptable — even ideal — for anticoagulants, since atrial fibrillation is overwhelmingly a senior condition, so the data captures a representative slice of the real market.

---

## Approach & Key Findings

### 1. Market structure
Eliquis dominates: **~$19.9B** in drug cost vs Xarelto's $5.4B, while warfarin's ~105K-prescriber base contributes almost nothing in dollars — making **warfarin conversion the cleanest revenue opportunity** for a new entrant.

### 2. Prescriber segmentation (the core insight)
Collapsed 511K rows to one row per prescriber, then cut into deciles by claims volume:

![Concentration Curve](charts/concentration_curve.png)

- **Top decile alone drives 49.5% of all claims.**
- **Top 3 deciles (30% of prescribers) drive 77.6%.**
- A top-decile prescriber is worth roughly **50x a bottom-decile one** — yet both cost a rep the same hour to visit. This concentration is the entire justification for targeting.

### 3. Target universe & salesforce sizing
- **Target universe:** deciles 8–10 -> **84,637 HCPs**.
- Primary care out-prescribes cardiology even in the elite tier, but cardiology is denser — supporting a **dual salesforce** (specialist + high-decile PCP).
- Tiered call frequency (12/8/4 visits/year by decile) -> **677,100 annual calls** / 1,400 rep capacity = **484 reps (~$121M field budget)**.

### 4. Territory design
Allocated reps to territories using the **largest-remainder method** — naive rounding drifted the total to 483; the algorithm reconciled it back to exactly 484. (Single-HCP jurisdictions — DC, PR, military codes — flagged as non-viable.)

### 5. Incentive compensation design
Modeled three payout curves against simulated territory attainment:

| Curve | Total Payout | vs Target Budget |
|---|---|---|
| Linear | $19.74M | +0.5% |
| Threshold-Accelerator | $18.68M | **-4.9%** |
| Capped Accelerator | $18.68M | -4.9% |

**Recommendation:** adopt the **threshold-accelerator** — it runs 4.9% under the $19.64M target budget, pays nothing below 80% attainment, and rewards overperformance at 2x above goal.

**Fairness flag:** the 80% threshold zeroes out **10 of 59 territories (17%)** — likely too punitive for a launch year with unvalidated goals. Recommended mitigations: lower the threshold to 70%, or introduce a partial payout band.

---

## Tech Stack

- **Python** — pandas, numpy (pipeline, segmentation, simulation, IC modeling)
- **matplotlib** — concentration curve visualization
- **Power BI** — executive dashboard (market concentration, HCP targeting, territory attainment, payout KPIs)

---

## Repository Structure

```
scripts/
  01pull_data.py       # CMS API extraction (511K rows)
  02clean_data.py      # cleaning, GE65 drop, dedup
  03explore_data.py    # market & specialty insights
  04segment_data.py    # collapse to prescribers, decile
  05target_sizing.py   # target universe + salesforce sizing
  06territory.py       # territory allocation (largest-remainder)
  07simulate.py        # synthetic commercial layer
  08incentive.py       # IC payout curves
  09dashboard_data.py  # dashboard data exports
  10charts.py          # concentration curve
charts/                # generated visuals
data/dashboard/        # dashboard-ready CSVs
notes.md               # decision log
```

*Raw data is not included (regenerable by running `01pull_data.py`).*

---

## How to Run

```bash
pip install pandas numpy matplotlib requests
python scripts/01pull_data.py      # pulls raw data from CMS API
python scripts/02clean_data.py     # run scripts in numbered order
# ... continue through 10charts.py
```

Each script consumes the previous stage's output — a reproducible pipeline.

# Pharma Brand Launch Analytics Dashboard
## 📊 Dashboard

An executive Power BI report covering the full launch decision — market
structure, prescriber targeting, salesforce sizing, and incentive payout.
## Dashboard Preview
<img width="1387" height="805" alt="dashboard_ph" src="https://github.com/user-attachments/assets/d053d321-c05e-498a-a46b-8e1e783320f9" />
**What it shows**
- **282,123 prescribers** segmented into deciles by claims volume
- **Top 30% of HCPs drive 77.6% of claims** — the core targeting thesis
- **484 reps / $19.64M IC budget** sized from tiered call frequency
- **Eliquis dominates** the market vs Xarelto & warfarin — the conversion play



