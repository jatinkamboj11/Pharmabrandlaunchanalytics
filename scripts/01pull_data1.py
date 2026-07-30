import requests
import pandas as pd
# Medicare Part D Prescribers - by Provider and Drug
BASE = "https://data.cms.gov/data-api/v1/dataset/9552739e-3d05-4c1b-8eff-ecabf391e2e5/data"
drugs = ["Eliquis", "Xarelto", "Warfarin Sodium",
         "Pradaxa", "Savaysa", "Jantoven"]
frames = []
for drug in drugs:
    offset = 0
    while True:
        params = {
            "filter[Brnd_Name]": drug,
            "size": 5000,
            "offset": offset
        }
        r = requests.get(BASE, params=params, timeout=60)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        frames.append(pd.DataFrame(batch))
        offset += 5000
        print(f"{drug}: {offset} rows pulled so far")
df = pd.concat(frames, ignore_index=True)
df.to_csv("raw_partd_anticoagulants.csv", index=False)
print("DONE")
print("Total rows:", df.shape[0])
print("Columns:", list(df.columns))     