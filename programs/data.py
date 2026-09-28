import os
import pandas as pd

from pybaseball import (
    batting_stats_bref,
    pitching_stats_bref,
    standings
)


START_YEAR = 2022
END_YEAR = 2025

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


def pull_batting_data():
    print("Pulling batting data...")

    data = pd.concat(
        [
            batting_stats_bref(year)
            for year in range(START_YEAR, END_YEAR + 1)
        ],
        ignore_index=True
    )

    data.to_csv(
        f"{DATA_DIR}/batting_raw.csv",
        index=False
    )

    print(f"Batting: {len(data)} rows, {len(data.columns)} columns")

    return data


def pull_pitching_data():
    print("Pulling pitching data...")

    data = pd.concat(
        [
            pitching_stats_bref(year)
            for year in range(START_YEAR, END_YEAR + 1)
        ],
        ignore_index=True
    )

    data.to_csv(
        f"{DATA_DIR}/pitching_raw.csv",
        index=False
    )

    print(f"Pitching: {len(data)} rows, {len(data.columns)} columns")

    return data


def pull_team_records():
    print("Pulling team records...")

    records = []

    for year in range(START_YEAR, END_YEAR + 1):
        print(f"  {year}")

        year_standings = standings(year)

        for division in year_standings:
            division = division.copy()
            division["Season"] = year
            records.append(division)

    data = pd.concat(records, ignore_index=True)

    data.to_csv(
        f"{DATA_DIR}/team_records_raw.csv",
        index=False
    )

    print(f"Team records: {len(data)} rows, {len(data.columns)} columns")

    return data


def main():
    pull_batting_data()
    pull_pitching_data()
    pull_team_records()

    print("\nData collection complete.")


if __name__ == "__main__":
    main()