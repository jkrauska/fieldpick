import pandas as pd
import logging
import sys
from frametools import analyze_columns, generate_schedules, check_consecutive, check_three_five, check_three_six, save_frame, check_three_seven

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

    check_three_five(cFrame, division)
    check_three_six(cFrame, division)
    #check_three_seven(cFrame, division)



from collections import Counter
dupe_check = Counter()
dropids = []
for row in cFrame.itertuples():

    dupe_check[row.Datestamp, row.Field] += 1
    if dupe_check[row.Datestamp, row.Field] > 1:
        print(row)
        print("DUPE FIELD FOUND")
        print(row.Datestamp, row.Field, row.index)

        dropids.append(row.Index)

        # Delete the row
# if dropids:
#     cFrame.drop(dropids, inplace=True)


# cFrame.sort_values(by=["Datestamp"], inplace=True, ignore_index=True)

# save_frame(cFrame, "calendar.pkl")
