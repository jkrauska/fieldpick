import pandas as pd
import logging
from helpers import short_division_names

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


def team_swap(cf, teamA, teamB):
    cf.replace(teamA, "TEMP_TEAM", inplace=True)
    cf.replace(teamB, teamA, inplace=True)
    cf.replace("TEMP_TEAM", teamB, inplace=True)
    return cf



# From lf10 to lf09
cFrame = team_swap(cFrame, "LowerFarm_10", "LowerFarm_09")
# LF05 LF01
cFrame = team_swap(cFrame, "LowerFarm_05", "LowerFarm_01")
# LF 08 LF 11
cFrame = team_swap(cFrame, "LowerFarm_08", "LowerFarm_11")

# Rookie08, Rookie10
cFrame= team_swap(cFrame, "Rookie_08", "Rookie_10")
# Rookie09, Rookie03
cFrame= team_swap(cFrame, "Rookie_09", "Rookie_03")
# Rookie04, Rookie01
cFrame= team_swap(cFrame, "Rookie_04", "Rookie_01")

# AAA01,AAA10
cFrame= team_swap(cFrame, "AAA_01", "AAA_10")

# Majors 05, Majors 07
cFrame= team_swap(cFrame, "Majors_05", "Majors_07")

save_frame(cFrame, "calendar.pkl")

