import os
import pandas as pd


DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data"
)

TEAMS = [
    "SEA", "TOR", "NYM", "SDP", "CLE", "TBR", "PHI", "STL",
    "NYY", "ATL", "HOU", "LAD", "MIN", "TEX", "ARI", "MIL",
    "MIA", "BAL", "KCR", "DET", "BOS", "CIN", "CHC"
]


def calculate_batting():

    df = pd.read_csv(
        os.path.join(DATA_DIR, "playoff_batting_players.csv")
    )

    df = df[df["Tm"].isin(TEAMS)].copy()

    team = df.groupby(
        ["Season", "Tm"],
        as_index=False
    ).agg({
        "PA": "sum",
        "AB": "sum",
        "R": "sum",
        "H": "sum",
        "2B": "sum",
        "3B": "sum",
        "HR": "sum",
        "RBI": "sum",
        "BB": "sum",
        "IBB": "sum",
        "SO": "sum",
        "HBP": "sum",
        "SF": "sum",
        "SB": "sum",
        "CS": "sum"
    })

    team["BA"] = team["H"] / team["AB"]

    team["OBP"] = (
        team["H"] +
        team["BB"] +
        team["HBP"]
    ) / (
        team["AB"] +
        team["BB"] +
        team["HBP"] +
        team["SF"]
    )

    team["SLG"] = (
        team["H"] +
        team["2B"] +
        2 * team["3B"] +
        3 * team["HR"]
    ) / team["AB"]

    team["OPS"] = team["OBP"] + team["SLG"]

    team["K%"] = team["SO"] / team["PA"]

    team["BB%"] = team["BB"] / team["PA"]

    team["ISO"] = team["SLG"] - team["BA"]

    team["wOBA"] = (
        0.69 * team["BB"] +
        0.72 * team["HBP"] +
        0.89 * (
            team["H"] -
            team["2B"] -
            team["3B"] -
            team["HR"]
        ) +
        1.27 * team["2B"] +
        1.62 * team["3B"] +
        2.10 * team["HR"]
    ) / (
        team["AB"] +
        team["BB"] -
        team["IBB"] +
        team["SF"] +
        team["HBP"]
    )

    return team


def calculate_pitching():

    df = pd.read_csv(
        os.path.join(DATA_DIR, "playoff_pitching_players.csv")
    )

    df = df[df["Tm"].isin(TEAMS)].copy()

    team = df.groupby(
        ["Season", "Tm"],
        as_index=False
    ).agg({
        "G": "sum",
        "GS": "sum",
        "W": "sum",
        "L": "sum",
        "SV": "sum",
        "IP": "sum",
        "H": "sum",
        "R": "sum",
        "ER": "sum",
        "BB": "sum",
        "SO": "sum",
        "HR": "sum",
        "HBP": "sum",
        "AB": "sum",
        "BF": "sum"
    })

    team["ERA"] = 9 * team["ER"] / team["IP"]

    team["WHIP"] = (
        team["BB"] +
        team["H"]
    ) / team["IP"]

    team["K%"] = team["SO"] / team["BF"]

    team["BB%"] = team["BB"] / team["BF"]

    team["K/BB"] = team["SO"] / team["BB"]

    team["HR/9"] = 9 * team["HR"] / team["IP"]

    team["BB/9"] = 9 * team["BB"] / team["IP"]

    team["SO/9"] = 9 * team["SO"] / team["IP"]

    team["H/9"] = 9 * team["H"] / team["IP"]

    team["BABIP"] = (
        team["H"] -
        team["HR"]
    ) / (
        team["AB"] -
        team["SO"] -
        team["HR"]
    )

    team["FIP"] = (
        13 * team["HR"] +
        3 * team["BB"] -
        2 * team["SO"]
    ) / team["IP"]

    return team


def calculate_team_stats(batting, pitching):

    batting = batting.rename(columns={
        "R": "Runs_Scored",
        "CS": "Batting_CS",
        "HR": "Batting_HR",
        "BB": "Batting_BB",
        "SO": "Batting_SO",
        "K%": "Batting_K%",
        "BB%": "Batting_BB%"
    })

    pitching = pitching.rename(columns={
        "R": "Runs_Allowed",
        "HR": "Pitching_HR",
        "BB": "Pitching_BB",
        "SO": "Pitching_SO",
        "K%": "Pitching_K%",
        "BB%": "Pitching_BB%"
    })

    team = batting.merge(
        pitching,
        on=["Season", "Tm"],
        how="inner"
    )

    team["Run_Differential"] = (
        team["Runs_Scored"] -
        team["Runs_Allowed"]
    )

    return team


def add_playoff_outcomes(team):

    playoffs = pd.read_csv(
        os.path.join(DATA_DIR, "22_25_playoff.csv")
    )

    playoffs = playoffs[
        ["Season", "Tm", "Wildcard", "DS", "CS", "WS"]
    ]

    return team.merge(
        playoffs,
        on=["Season", "Tm"],
        how="inner"
    )


def find_correlations(df):

    outcomes = [
        "DS",
        "CS",
        "WS"
    ]

    excluded = {
        "Season",
        "Tm",
        "Wildcard",
        "DS",
        "CS",
        "WS"
    }

    metrics = [
        column
        for column in df.columns
        if column not in excluded
        and pd.api.types.is_numeric_dtype(df[column])
    ]

    results = []

    for outcome in outcomes:

        for metric in metrics:

            if df[metric].nunique() < 2:
                continue

            if df[outcome].nunique() < 2:
                continue

            correlation = df[metric].corr(df[outcome])

            if pd.notna(correlation):

                results.append({
                    "Round": outcome,
                    "Metric": metric,
                    "Correlation": correlation,
                    "Absolute_Correlation": abs(correlation)
                })

    results = pd.DataFrame(results)

    return results.sort_values(
        ["Round", "Absolute_Correlation"],
        ascending=[True, False]
    )


def print_results(correlations):

    print("\n" + "=" * 50)
    print("HIGHEST CORRELATIONS WITH PLAYOFF ADVANCEMENT")
    print("=" * 50)

    for round_name, label in [
        ("DS", "Division Series"),
        ("CS", "Championship Series"),
        ("WS", "World Series")
    ]:

        print(f"\n{label}")
        print("-" * len(label))

        results = correlations[
            correlations["Round"] == round_name
        ].head(5)

        for _, row in results.iterrows():

            direction = "Positive" if row["Correlation"] > 0 else "Negative"

            print(
                f"{row['Metric']:<22} "
                f"{row['Correlation']:>7.3f}  "
                f"{direction}"
            )


def main():

    print("Calculating batting statistics...")
    batting = calculate_batting()

    print("Calculating pitching statistics...")
    pitching = calculate_pitching()

    print("Combining team statistics...")
    team = calculate_team_stats(
        batting,
        pitching
    )

    print("Adding playoff outcomes...")
    team = add_playoff_outcomes(team)

    team.to_csv(
        os.path.join(DATA_DIR, "team_analysis.csv"),
        index=False
    )

    correlations = find_correlations(team)

    correlations.to_csv(
        os.path.join(DATA_DIR, "correlations.csv"),
        index=False
    )

    print_results(correlations)

    print("\n")
    print(f"Team-season observations: {len(team)}")
    print("Full team dataset: data/team_analysis.csv")
    print("Full correlation dataset: data/correlations.csv")


if __name__ == "__main__":
    main()