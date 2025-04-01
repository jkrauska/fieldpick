from collections import Counter
import pandas as pd
import logging
import sys
from frametools import analyze_columns, generate_schedules, check_consecutive, check_three_six, save_frame

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
    print(division)
    check_consecutive(cFrame, division)
    check_three_six(cFrame, division, size=6)

    team_names_a = sorted(list(division_frame['Away_Team'].unique()))

    for compare_division, compare_division_frame in divisionFrames.items():
        if division == compare_division:
            continue
        team_names_b = sorted(
            list(compare_division_frame['Away_Team'].unique()))
        for teamA in team_names_a:
            for teamB in team_names_b:

                a_starts = division_frame.query(
                    f"Home_Team == '{teamA}' or Away_Team == '{teamA}'")
                b_starts = compare_division_frame.query(
                    f"Home_Team == '{teamB}' or Away_Team == '{teamB}'")

                atimes = a_starts['Datestamp'].astype(int).values
                btimes = b_starts['Datestamp'].astype(int).values

                min_delta = 999999999999
                for i in atimes:
                    # print(atimes)
                    for j in btimes:
                        delta = int(abs(i - j) / 1000000000 / 60)
                        min_delta = min(delta, min_delta)

                if min_delta > 120:
                    print(f"Min {min_delta},A,{teamA},B,{teamB}")


dupe_check = Counter()
dropids = []
for row in cFrame.itertuples():

    dupe_check[row.Datestamp, row.Full_Field] += 1
    if dupe_check[row.Datestamp, row.Full_Field] > 1:
        print(row)
        print("DUPE FIELD FOUND")
        print(row.Datestamp, row.Full_Field, row.index)

        dropids.append(row.Index)

        # Delete the row
# if dropids:
#     cFrame.drop(dropids, inplace=True)


# cFrame.sort_values(by=["Datestamp"], inplace=True, ignore_index=True)

# save_frame(cFrame, "calendar.pkl")
