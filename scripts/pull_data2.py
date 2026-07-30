import requests
import pandas as pd

# Step 1: find the CURRENT dataset endpoint by searching CMS's catalog
CATALOG_URL = "https://data.cms.gov/data.json"
print("Looking up current dataset location...")
catalog = requests.get(CATALOG_URL, timeout=60).json()

target_title = "Medicare Part D Prescribers - by Provider and Drug"
api_url = None

for ds in catalog["dataset"]:
    if target_title.lower() in ds.get("title", "").lower():
        for dist in ds["distribution"]:
            if dist.get("format") == "API" and dist.get("description") == "latest":
                api_url = dist["accessURL"]
                break
        if api_url:
            break

if not api_url:
    raise RuntimeError("Could not find the dataset automatically — check the title text.")

print(f"Found current endpoint: {api_url}")

# Step 2: pull our six drugs from that endpoint
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
        r = requests.get(api_url, params=params, timeout=60)
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