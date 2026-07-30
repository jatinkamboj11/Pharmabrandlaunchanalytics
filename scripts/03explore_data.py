import pandas as pd

df = pd.read_csv("data/clean/clean_partd_anticoagulants.csv", dtype={"Prscrbr_NPI": str, "Prscrbr_State_FIPS": str})

print(df.shape)
print(df.head())
print(df["Brnd_Name"].value_counts())

print(df.groupby("Brnd_Name")["Tot_Clms"].sum().sort_values(ascending=False))

print((df.groupby("Brnd_Name")["Tot_Drug_Cst"].sum() / 1e9).round(2))

print(df.groupby("Prscrbr_Type")["Tot_Clms"].sum().sort_values(ascending=False).head(10))