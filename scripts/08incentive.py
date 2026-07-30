import pandas as pd
import numpy as np

terr = pd.read_csv("data/clean/territories.csv")

terr["reps"] = (terr["planned_calls"] / 1400).round().clip(lower=1)
TARGET_BONUS = 40000
terr["target_incentive"] = terr["reps"] * TARGET_BONUS

att = terr["attainment_pct"]

terr["payout_linear"] = terr["target_incentive"] * att / 100

factor_accel = np.select(
    [att < 80, att <= 100],
    [0, att],
    default=100 + 2 * (att - 100)
)
terr["payout_accel"] = terr["target_incentive"] * factor_accel / 100

att_capped = att.clip(upper=150)
factor_capped = np.select(
    [att_capped < 80, att_capped <= 100],
    [0, att_capped],
    default=100 + 2 * (att_capped - 100)
)
terr["payout_capped"] = terr["target_incentive"] * factor_capped / 100

print("Target budget: $", round(terr["target_incentive"].sum()))
print("Linear:        $", round(terr["payout_linear"].sum()))
print("Accelerator:   $", round(terr["payout_accel"].sum()))
print("Capped:        $", round(terr["payout_capped"].sum()))

terr["diff_vs_linear"] = terr["payout_accel"] - terr["payout_linear"]

print("\nBiggest LOSERS under accelerator:")
print(terr.nsmallest(5, "diff_vs_linear")[["state", "attainment_pct", "payout_linear", "payout_accel"]].round(0))

print("\nBiggest WINNERS under accelerator:")
print(terr.nlargest(5, "diff_vs_linear")[["state", "attainment_pct", "payout_accel", "payout_linear"]].round(0))

print("\nTerritories paid ZERO:", (terr["payout_accel"] == 0).sum())

terr.to_csv("data/clean/incentive_results.csv", index=False)
print("Saved incentive_results.csv")
