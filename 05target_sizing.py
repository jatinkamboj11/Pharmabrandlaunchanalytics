import pandas as pd

hcp = pd.read_csv("data/clean/hcp_segmented.csv", dtype={"Prscrbr_NPI": str})

targets = hcp[hcp["decile"] >= 8]

print(targets.shape)
print(targets["specialty"].value_counts().head(10))
print(targets["state"].value_counts().head(10))


call_freq = {8: 4, 9: 8, 10: 12}
targets = targets.copy()
targets["planned_calls"] = targets["decile"].map(call_freq)

total_calls = targets["planned_calls"].sum()
reps_needed = total_calls / 1400

print("Total annual calls needed:", total_calls)
print("Reps needed:", round(reps_needed))

targets.to_csv("data/clean/targets.csv", index=False)
print("Saved targets.csv")