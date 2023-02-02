import pandas as pd
import logging
import sys
from frametools import analyze_columns, generate_schedules
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

publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")


aFrame = analyze_columns(cFrame)
publish_df_to_gsheet(aFrame, worksheet_name="Analysis")

uFrame = cFrame.query("Division != Division")
publish_df_to_gsheet(uFrame, worksheet_name="Unassigned")

import time
time.sleep(3)

divisionFrames = generate_schedules(cFrame)
for division, division_frame in divisionFrames.items():
    drop_columns = [
        'Week_Number', 'Time_Length', 'Day_of_Year', 'Division', "Home_Team", "Away_Team",
        'Notes',	'location',	'size',	'type',	'infield']

    division_frame = division_frame.drop(columns=drop_columns)
    publish_df_to_gsheet(division_frame, worksheet_name=f"{division}")
    logger.info("Sleeping for 10 second to avoid rate limit")
    time.sleep(10)
