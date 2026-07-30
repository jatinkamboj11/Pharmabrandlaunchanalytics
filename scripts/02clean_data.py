import pandas as pd

df = pd.read_csv("data/raw/raw_partd_anticoagulants.csv", dtype={"Prscrbr_NPI": str, "Prscrbr_State_FIPS": str})
print(df.shape)

ge65_cols = [c for c in df.columns if c.startswith("GE65")]
df = df.drop(columns=ge65_cols)
df = df.drop(columns=["Prscrbr_Type_Src"])
print(df.shape)

dupes = df.duplicated(subset=["Prscrbr_NPI", "Brnd_Name"]).sum()
print("Duplicates:", dupes)

df.to_csv("data/clean/clean_partd_anticoagulants.csv", index=False)
print("Saved.")