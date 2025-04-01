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
from inputs import division_info
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


# Data cleanup
tidy = (pd.isna(cFrame["Division"]))
slot_mask = tidy

slots_to_clear = cFrame[slot_mask].index


for i in slots_to_clear:
    # Home_Team	Home_Team_Name	Away_Team	Away_Team_Name
    cFrame.loc[i, "Home_Team"] = None
    cFrame.loc[i, "Home_Team_Name"] = None
    cFrame.loc[i, "Away_Team"] = None
    cFrame.loc[i, "Away_Team_Name"] = None

    cFrame.loc[i, "Game_ID"] = f"NONE-9{i:03d}"


save_frame(cFrame, "calendar.pkl")
publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")
aFrame = analyze_columns(cFrame)


publish_df_to_gsheet(aFrame, worksheet_name="Analysis")
uFrame = cFrame.query("Division != Division")
publish_df_to_gsheet(uFrame, worksheet_name="Unassigned")
