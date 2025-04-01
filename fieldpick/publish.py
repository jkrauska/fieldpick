import pandas as pd
import logging
from gsheets import publish_df_to_gsheet


logging.basicConfig(
    format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO)
logger = logging.getLogger()


# Load calendar
logger.info("Loading calendar data")
save_file = "data/calendar.pkl"
cFrame = pd.read_pickle(save_file)

publish_df_to_gsheet(cFrame)
