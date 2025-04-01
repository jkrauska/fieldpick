import pandas as pd
import logging
from frametools import (
    analyze_columns,
    swap_rows_by_game_id,
    balance_home_away,
    swap_rows_by_slot,
    list_teams_for_division,
    assign_row,
    clear_division,
)
from gsheets import publish_df_to_gsheet
from helpers import short_division_names
from inputs import division_info, team_names
import re
from pulp import *
from collections import Counter


from frametools import (
    save_frame,
)
from gsheets import publish_df_to_gsheet


logging.basicConfig(
    format="%(asctime)s %(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger()


# Load calendar
logger.info("Loading calendar data")
save_file = "data/calendar.pkl"
cFrame = pd.read_pickle(save_file)
print(f"Loaded {len(cFrame)} slots")


for slot in cFrame.index:
    if cFrame.loc[slot, "Division"]:
        division = cFrame.loc[slot, "Division"]
        if division == "Challenger":
            cFrame.loc[slot, "Home_Team_Name"] = "Challenger"
            cFrame.loc[slot, "Home_Team"] = "Challenger"

            cFrame.loc[slot, "Away_Team_Name"] = "Challenger"
            cFrame.loc[slot, "Away_Team"] = "Challenger"

        if division not in team_names:
            continue
        if cFrame.loc[slot, "Home_Team"]:
            home_team = cFrame.loc[slot, "Home_Team"]
            if home_team in team_names[division]:
                cFrame.loc[slot,
                           "Home_Team_Name"] = team_names[division][home_team]
        if cFrame.loc[slot, "Away_Team"]:
            away_team = cFrame.loc[slot, "Away_Team"]
            if away_team in team_names[division]:
                cFrame.loc[slot,
                           "Away_Team_Name"] = team_names[division][away_team]


# sys.exit(1)

save_frame(cFrame, "calendar.pkl")
publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")
# aFrame = analyze_columns(cFrame)
# publish_df_to_gsheet(aFrame, worksheet_name="Analysis")
# uFrame = cFrame.query("Division != Division")
# publish_df_to_gsheet(uFrame, worksheet_name="Unassigned")
