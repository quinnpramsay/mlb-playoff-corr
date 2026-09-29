import pandas as pd
import glob
import os

for file in glob.glob("data/*.csv"):
    try:
        df = pd.read_csv(file)

        if "Tm" not in df.columns:
            continue

        counts = df["Tm"].value_counts()

        nym = counts.get("NYM", 0)
        nyy = counts.get("NYY", 0)
        new_york = counts.get("New York", 0)

        if nym > 0 or nyy > 0 or new_york > 0:
            print(f"\n{os.path.basename(file)}")
            print(f"  NYM:      {nym}")
            print(f"  NYY:      {nyy}")
            print(f"  New York: {new_york}")

    except Exception as e:
        print(f"Error reading {file}: {e}")