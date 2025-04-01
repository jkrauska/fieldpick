import pandas as pd
import logging
import sys
import time
from frametools import analyze_columns, generate_schedules, load_frame
from gsheets import publish_df_to_gsheet


logging.basicConfig(
    format="%(asctime)s %(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger()


# Load calendar
cFrame = load_frame("data/calendar.pkl")


scFrame = cFrame.copy()

keep_columns = [
    'Week_Number',
    'Home_Team',
    'Away_Team',
    'Date',
    'Start',
    'End',
    'Location',
    'Field',
]
scFrame = scFrame[keep_columns]
scFrame.dropna(subset=['Home_Team'], inplace=True)

scFrame.rename(columns={'Week_Number': 'RoundNo'}, inplace=True)
scFrame.rename(columns={'Home_Team': 'HomeTeam'}, inplace=True)
scFrame.rename(columns={'Away_Team': 'AwayTeam'}, inplace=True)
scFrame.rename(columns={'Date': 'MatchDate'}, inplace=True)
scFrame.rename(columns={'Start': 'StartTime'}, inplace=True)
scFrame.rename(columns={'End': 'EndTime'}, inplace=True)
scFrame.index.name = "SortOrder"


# for col in scFrame.columns:
#     if col not in keep_columns:
#         print(col)
#         scFrame = scFrame.drop(columns=col)
print(scFrame)
scFrame.to_csv('sportsConnect.csv', index=True)


# sys.exit(1)

aFrame = analyze_columns(cFrame)
publish_df_to_gsheet(aFrame, worksheet_name="Analysis")

uFrame = cFrame.query("Division != Division")
publish_df_to_gsheet(uFrame, worksheet_name="Unassigned")

# time.sleep(3)

divisionFrames = generate_schedules(cFrame)
for division, division_frame in divisionFrames.items():
    drop_columns = [
        'Week_Number', 'Time_Length', 'Intended_Division',
        'Day_of_Year', 'Division', "Datestamp",
        "Home_Team", "Away_Team",
        'Notes', 'Location', 'Field', 'Size',
        'Type', 'Infield', 'Sunset', 'Region'
    ]
    for col in drop_columns:
        if col in division_frame.columns:
            division_frame = division_frame.drop(columns=col)
    publish_df_to_gsheet(division_frame, worksheet_name=f"{division}")
    logger.info("Sleeping for 10 second to avoid rate limit")
    time.sleep(10)
