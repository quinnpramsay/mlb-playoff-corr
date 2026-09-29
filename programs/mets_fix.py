import pandas as pd


URLS = {
    2022: "https://www.baseball-reference.com/teams/NYM/2022.shtml",
    2024: "https://www.baseball-reference.com/teams/NYM/2024.shtml"
}


def get_mets_players():
    mets_players = {}

    for year, url in URLS.items():
        print(f"Pulling Mets roster for {year}...")

        tables = pd.read_html(url)

        players = set()

        for table in tables:
            if "Player" in table.columns:
                players.update(
                    table["Player"]
                    .dropna()
                    .astype(str)
                    .str.replace(r"[*#?]", "", regex=True)
                )

            if "Name" in table.columns:
                players.update(
                    table["Name"]
                    .dropna()
                    .astype(str)
                    .str.replace(r"[*#?]", "", regex=True)
                )

        players.discard("Team Totals")
        mets_players[year] = players

        print(f"{year}: {len(players)} players found")

    return mets_players


def fix_new_york(df, mets_players):

    for index, row in df.iterrows():

        if "New York" not in row["Tm"]:
            continue

        season = row["Season"]
        player = row["Name"]

        player = str(player).replace("*", "").replace("#", "").replace("?", "").strip()

        if season in mets_players and player in mets_players[season]:
            df.at[index, "Tm"] = row["Tm"].replace("New York", "NYM")
        else:
            df.at[index, "Tm"] = row["Tm"].replace("New York", "NYY")

    return df


def main():

    # Get Mets rosters once
    mets_players = get_mets_players()

    # Fix batting
    batting = pd.read_csv("data/playoff_batting_players.csv")
    batting = fix_new_york(batting, mets_players)
    batting.to_csv(
        "data/playoff_batting_players.csv",
        index=False
    )

    print("Batting teams fixed.")

    # Fix pitching
    pitching = pd.read_csv("data/playoff_pitching_players.csv")
    pitching = fix_new_york(pitching, mets_players)
    pitching.to_csv(
        "data/playoff_pitching_players.csv",
        index=False
    )

    print("Pitching teams fixed.")

    print("\nNew York teams fixed.")


if __name__ == "__main__":
    main()