import pandas as pd


batting_df = pd.read_csv("data/batting_team_raw.csv")
pitching_df = pd.read_csv("data/pitching_team_raw.csv")


TEAM_MAP = {
    "SEA": "Seattle",
    "TOR": "Toronto",
    "NYM": "New York",
    "SDP": "San Diego",
    "CLE": "Cleveland",
    "TBR": "Tampa Bay",
    "PHI": "Philadelphia",
    "STL": "St. Louis",
    "NYY": "New York",
    "ATL": "Atlanta",
    "HOU": "Houston",
    "LAD": "Los Angeles",
    "MIN": "Minnesota",
    "TEX": "Texas",
    "ARI": "Arizona",
    "MIL": "Milwaukee",
    "MIA": "Miami",
    "BAL": "Baltimore",
    "KCR": "Kansas City",
    "DET": "Detroit",
    "BOS": "Boston",
    "CIN": "Cincinnati",
    "CHC": "Chicago"
}


PLAYOFF_TEAMS = list(TEAM_MAP.keys())


def get_playoff_players(df):
    teams = list(TEAM_MAP.values())

    pattern = "|".join(teams)

    return df[
        df["Tm"].str.contains(
            pattern,
            case=False,
            na=False
        )
    ].copy()


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