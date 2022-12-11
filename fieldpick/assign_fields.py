import pandas as pd
import logging
import random



logging.basicConfig(
    format="%(asctime)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO
)
logger = logging.getLogger()


# Load calendar
logger.info("Loading calendar"
save_file = "data/calendar.pkl"
cFrame = pd.read_pickle(save_file)

# Load division data
logger.info("Loading teams")
save_file = "data/teams.pkl"
tFrame = pd.from_pickle(save_file)

