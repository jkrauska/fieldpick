import pandas as pd
import logging
import sys
from frametools import analyze_columns, generate_schedules, check_consecutive

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

divisionFrames = generate_schedules(cFrame)
for division, division_frame in divisionFrames.items():
    check_consecutive(cFrame, division)