
import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("charts", exist_ok=True)

dec = pd.read_csv("data/dashboard/decile_concentration.csv")
dec = dec.sort_values("decile", ascending=False)

fig, ax1 = plt.subplots(figsize=(9, 5))

ax1.bar(dec["decile"].astype(str), dec["claims_share_pct"], color="#4C72B0")
ax1.set_xlabel("Prescriber Decile (10 = highest volume)")
ax1.set_ylabel("Share of Claims (%)")

ax2 = ax1.twinx()
ax2.plot(dec["decile"].astype(str), dec["cumulative_share_pct"],
         color="#C44E52", marker="o", linewidth=2)
ax2.set_ylabel("Cumulative Share (%)")
ax2.set_ylim(0, 105)

plt.title("Prescriber Concentration: Top 30% Drive 77.6% of Claims")
plt.tight_layout()
plt.savefig("charts/concentration_curve.png", dpi=150)
print("Saved charts/concentration_curve.png")

