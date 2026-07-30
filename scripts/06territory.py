import pandas as pd

targets = pd.read_csv("data/clean/targets.csv", dtype={"Prscrbr_NPI": str})

state_calls = targets.groupby("state")["planned_calls"].sum().sort_values(ascending=False)

state_reps = (state_calls / 1400).round()

print(state_reps.head(15))
print("Total reps across states:", state_reps.sum())

import numpy as np

exact = state_calls / 1400
floors = np.floor(exact)
remainders = exact - floors

shortfall = 484 - int(floors.sum())
print("Reps still to award after flooring:", shortfall)

winners = remainders.sort_values(ascending=False).head(shortfall)
print("States awarded the extra reps:")
print(winners.round(3))