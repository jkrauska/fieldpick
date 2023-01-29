import pandas as pd
import logging
from frametools import analyze_columns
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

aFrame = analyze_columns(cFrame)
publish_df_to_gsheet(aFrame, worksheet_name="Analysis")
