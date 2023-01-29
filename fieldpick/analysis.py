import pandas as pd
import logging
import sys
from inputs import division_info
from frametools import list_teams_for_division, weeks_in_season, save_frame, score_frame, clear_division, analyze_columns
from faceoffs import faceoffs_repeated
from gsheets import publish_df_to_gsheet


from random import shuffle, seed

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

aFrame = analyze_columns(cFrame)
publish_df_to_gsheet(aFrame, worksheet_name="Analysis")
