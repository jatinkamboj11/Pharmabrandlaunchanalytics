import pandas as pd
import os

os.makedirs("data/dashboard", exist_ok=True)

clean = pd.read_csv("data/clean/clean_partd_anticoagulants.csv")
hcp = pd.read_csv("data/clean/hcp_segmented.csv", dtype={"Prscrbr_NPI": str})
targets = pd.read_csv("data/clean/targets.csv", dtype={"Prscrbr_NPI": str})
ic = pd.read_csv("data/clean/incentive_results.csv")

# 1. Market view
market = clean.groupby("Brnd_Name").agg(
    prescribers=("Prscrbr_NPI", "count"),
    claims=("Tot_Clms", "sum"),
    cost=("Tot_Drug_Cst", "sum")
).reset_index()
market["cost_share_pct"] = (market["cost"] / market["cost"].sum() * 100).round(1)
market.to_csv("data/dashboard/market_by_drug.csv", index=False)

# 2. Concentration curve
dec = hcp.groupby("decile").agg(
    hcps=("Prscrbr_NPI", "count"),
    claims=("total_claims", "sum")
).reset_index()
dec["claims_share_pct"] = (dec["claims"] / dec["claims"].sum() * 100).round(1)
dec = dec.sort_values("decile", ascending=False)
dec["cumulative_share_pct"] = dec["claims_share_pct"].cumsum().round(1)
dec.to_csv("data/dashboard/decile_concentration.csv", index=False)

# 3. Target profile by specialty
spec = targets.groupby("specialty").agg(
    targets=("Prscrbr_NPI", "count"),
    claims=("total_claims", "sum"),
    planned_calls=("planned_calls", "sum")
).reset_index().sort_values("targets", ascending=False)
spec.to_csv("data/dashboard/target_by_specialty.csv", index=False)

# 4. Territory + IC (already built)
ic.to_csv("data/dashboard/territory_ic.csv", index=False)

print("Exported 4 dashboard files")
print(dec[["decile", "claims_share_pct", "cumulative_share_pct"]])