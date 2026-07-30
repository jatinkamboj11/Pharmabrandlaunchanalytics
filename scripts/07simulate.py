import pandas as pd
import numpy as np

np.random.seed(42)

targets = pd.read_csv("data/clean/targets.csv", dtype={"Prscrbr_NPI": str})

terr = targets.groupby("state").agg(
    hcps=("Prscrbr_NPI", "count"),
    planned_calls=("planned_calls", "sum"),
    market_claims=("total_claims", "sum")
).reset_index()

print(terr.shape)
print(terr.head())




NATIONAL_GOAL_SHARE = 0.03
terr["goal_claims"] = (terr["market_claims"] * NATIONAL_GOAL_SHARE).round()

terr["attainment_pct"] = np.random.normal(loc=100, scale=18, size=len(terr)).clip(55, 160).round(1)

terr["actual_claims"] = (terr["goal_claims"] * terr["attainment_pct"] / 100).round()

print(terr[["state", "goal_claims", "attainment_pct", "actual_claims"]].head(10))
print("\nAttainment stats:")
print(terr["attainment_pct"].describe().round(1))

terr.to_csv("data/clean/territories.csv", index=False)
print("Saved territories.csv —", terr.shape)