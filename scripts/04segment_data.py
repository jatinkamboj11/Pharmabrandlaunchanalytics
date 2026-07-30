import pandas as pd

df = pd.read_csv("data/clean/clean_partd_anticoagulants.csv", dtype={"Prscrbr_NPI": str, "Prscrbr_State_FIPS": str})

hcp = df.groupby("Prscrbr_NPI").agg(
    total_claims=("Tot_Clms", "sum"),
    total_cost=("Tot_Drug_Cst", "sum"),
    specialty=("Prscrbr_Type", "first"),
    state=("Prscrbr_State_Abrvtn", "first")
).reset_index()

print(hcp.shape)
print(hcp.head())

hcp["decile"] = pd.qcut(hcp["total_claims"].rank(method="first"), 10, labels=False) + 1

print(hcp["decile"].value_counts().sort_index())


decile_claims = hcp.groupby("decile")["total_claims"].sum()
share = (decile_claims / decile_claims.sum() * 100).round(1)
print(share)

print("Top 3 deciles (30% of doctors) control:", share[8] + share[9] + share[10], "% of all claims")

hcp.to_csv("data/clean/hcp_segmented.csv", index=False)
print("Saved hcp_segmented.csv")