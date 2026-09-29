import pandas as pd

batting_df = pd.read_csv("data/batting_team_raw.csv")
pitching_df = pd.read_csv("data/pitching_team_raw.csv")


TEAM_MAP = {
    "Seattle": "SEA",
    "Toronto": "TOR",
    "San Diego": "SDP",
    "Cleveland": "CLE",
    "Tampa Bay": "TBR",
    "Philadelphia": "PHI",
    "St. Louis": "STL",
    "Atlanta": "ATL",
    "Houston": "HOU",
    "Los Angeles": "LAD",
    "Minnesota": "MIN",
    "Texas": "TEX",
    "Arizona": "ARI",
    "Milwaukee": "MIL",
    "Miami": "MIA",
    "Baltimore": "BAL",
    "Kansas City": "KCR",
    "Detroit": "DET",
    "Boston": "BOS",
    "Cincinnati": "CIN",
    "Chicago": "CHC",
    "New York": "New York",
}


PLAYOFF_TEAMS = list(TEAM_MAP.keys())


def get_playoff_players(df):
    pattern = "|".join(PLAYOFF_TEAMS)

    df = df[
        df["Tm"].str.contains(
            pattern,
            case=False,
            na=False
        )
    ].copy()

    for team_name, team_code in TEAM_MAP.items():
        df["Tm"] = df["Tm"].str.replace(
            team_name,
            team_code,
            regex=False
        )

    return df


batting_playoff = get_playoff_players(batting_df)
pitching_playoff = get_playoff_players(pitching_df)


batting_playoff.to_csv(
    "data/playoff_batting_players.csv",
    index=False
)

pitching_playoff.to_csv(
    "data/playoff_pitching_players.csv",
    index=False
)


print("Complete.")
print(f"Batting rows: {len(batting_playoff)}")
print(f"Pitching rows: {len(pitching_playoff)}")