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

# Swap games on Fridays at Fort Scott North and South Sunset D1
friday_games = cFrame[(cFrame['Day_of_Week'] == 'Friday') & 
                        (cFrame['Full_Field'].isin(['Fort Scott - North Diamond', 'South Sunset - Diamond 1'])) &
                        (cFrame['Division'].notna())]

for date in friday_games['Date'].unique():
    games_on_date = friday_games[friday_games['Date'] == date]
    if len(games_on_date['Full_Field'].unique()) == 2:
        field1, field2 = games_on_date['Full_Field'].unique()
        temp_location1 = games_on_date.loc[games_on_date['Full_Field'] == field1, 'Location'].values[0]
        temp_field1 = games_on_date.loc[games_on_date['Full_Field'] == field1, 'Field'].values[0]
        temp_full_field1 = games_on_date.loc[games_on_date['Full_Field'] == field1, 'Full_Field'].values[0]
        temp_location2 = games_on_date.loc[games_on_date['Full_Field'] == field2, 'Location'].values[0]
        temp_field2 = games_on_date.loc[games_on_date['Full_Field'] == field2, 'Field'].values[0]
        temp_full_field2 = games_on_date.loc[games_on_date['Full_Field'] == field2, 'Full_Field'].values[0]

        games_on_date.loc[games_on_date['Full_Field'] == field2, 'Full_Field'] = 'TEMP_FIELD'
        games_on_date.loc[games_on_date['Full_Field'] == field1, ['Full_Field', 'Location', 'Field']] = [temp_full_field2, temp_location2, temp_field2]
        games_on_date.loc[games_on_date['Full_Field'] == 'TEMP_FIELD', ['Full_Field', 'Location', 'Field']] = [temp_full_field1, temp_location1, temp_field1]
        cFrame.update(games_on_date)

new_friday_games = cFrame[(cFrame['Day_of_Week'] == 'Friday') & (cFrame['Full_Field'].isin(['Fort Scott - North Diamond', 'South Sunset - Diamond 1']))]
print(new_friday_games[['Date', 'Full_Field', 'Location', 'Field', 'Home_Team', 'Away_Team', 'Intended_Division', 'Division']])

# save_frame(cFrame, "calendar.pkl")
