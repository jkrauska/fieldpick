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

from datetime import datetime
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
# logger.info("Loading calendar data")
save_file = "data/calendar.pkl"
cFrame = pd.read_pickle(save_file)
# print(f"Loaded {len(cFrame)} slots")


majors = cFrame["Division"] == "Majors"

working_slots = cFrame[majors].index
# print(f"Working with {len(working_slots)} slots")


print("date,time,home,away,location,duration")
for slot in working_slots:
    # print(slot)

    date_str = cFrame.loc[slot, "Date"]
    datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
    new_date_str = datetime_obj.strftime('%-m/%-d/%Y')

    time_str = cFrame.loc[slot, "Game_Start"]
    datetime_obj = datetime.strptime(time_str, '%H:%M')
    new_time_str = datetime_obj.strftime('%-I:%M %p')

    home = cFrame.loc[slot, "Home_Team_Name"]
    if home == "Athletics":
        home = "A's"
    if home == "Angels":
        home_str = f"SFLL Majors {home}"
    else:
        home_str = f"SFLL Majors {home} Spring 2025"

    away = cFrame.loc[slot, "Away_Team_Name"]
    if away == "Athletics":
        away = "A's"
    if away == "Angels":
        away_str = f"SFLL Majors {away}"
    else:
        away_str = f"SFLL Majors {away} Spring 2025"

    field = cFrame.loc[slot, "Field"]
    if "Kimbell" in field:
        field += ", 1901 Geary Blvd, San Francisco, CA 94115"
    elif "South Sunset" in field:
        field += ", 40th Ave &, Vicente St, San Francisco, CA 94116"
    elif "Ft. Scott" in field:
        field += ", 1299 Storey Ave, San Francisco, CA 94129"
    elif "Tepper" in field:
        field += ", 849 4th St, San Francisco, CA 94130"
    elif "Ketcham" in field:
        field += ", 8th Street, Avenue M, San Francisco, CA 94130"

    print(f"{new_date_str},{new_time_str},{home_str},{away_str},\"{field}\",120")
