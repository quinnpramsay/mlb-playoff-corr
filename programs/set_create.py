import pandas as pd
import numpy as np

batting_df = pd.read_csv('batting_raw.csv')
pitching_df = pd.read_csv('pitching_raw.csv')
records_df = pd.read_csv('team_records_raw.csv')
playoffs_df = pd.read_csv('22_25_playoff.csv')

teams = ["SEA", "TOR", "NYM", "SDP", "CLE", "TBR", "PHI", "STL", "NYY", "ATL", "HOU", "LAD", "MIN", "TEX", "ARI", "MIL", "MIA", "BAL", "KCR", "DET", "BOS", "CIN", "CHC"]

batting_df = batting_df[batting_df["Tm"].isin(teams)]
pitching_df = pitching_df[pitching_df["Tm"].isin(teams)]
records_df = records_df[records_df["Tm"].isin(teams)]
playoffs_df = playoffs_df[playoffs_df["Tm"].isin(teams)]

