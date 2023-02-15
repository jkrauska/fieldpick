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

import datetime as dt


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



#cFrame.insert(5, "Game_Start", 0)

for slot in cFrame.index:
    field_start = cFrame.loc[slot, "Start"]
    field_start_dt = dt.datetime.strptime(field_start, '%H:%M')

    Time_Length = cFrame.loc[slot, "Time_Length"]
    if Time_Length == "90" or Time_Length == "120":
        game_start = field_start_dt + dt.timedelta(minutes=15)
    else:
        game_start = field_start_dt + dt.timedelta(minutes=30)

    cFrame.loc[slot, "Game_Start"] = game_start.strftime('%H:%M')


    #print(cFrame.loc[slot])



#sys.exit(1)

save_frame(cFrame, "calendar.pkl")
publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")
# aFrame = analyze_columns(cFrame)
# publish_df_to_gsheet(aFrame, worksheet_name="Analysis")
# uFrame = cFrame.query("Division != Division")
# publish_df_to_gsheet(uFrame, worksheet_name="Unassigned")
