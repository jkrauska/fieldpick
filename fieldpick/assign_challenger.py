import pandas as pd

import logging
from inputs import division_info
from frametools import (
    list_teams_for_division,
    weeks_in_season,
    save_frame,
    score_frame,
    reserve_slots,
    check_consecutive,
    score_gamecount,
)
from faceoffs import faceoffs_repeated
from gsheets import publish_df_to_gsheet
from datetime import datetime
from helpers import tepper_ketcham, short_division_names

from collections import defaultdict


from random import shuffle, seed

import numpy as np


logging.basicConfig(
    format="%(asctime)s %(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger()


def clear_row(frame, slot):
    frame.loc[slot,
              ["Division",
               "Home_Team",
               "Home_Team_Name",
               "Away_Team",
               "Away_Team_Name",
               "Game_ID"]] = [None,
                              None,
                              None,
                              None,
                              None,
                              None,
                              ]

# @profile


def main():
    # Main loop

    # Load calendar
    logger.info("Loading calendar data")
    save_file = "data/calendar.pkl"
    cFrame = pd.read_pickle(save_file)
    print(f"Loaded {len(cFrame)} slots")

    # Load division data
    logger.info("Loading teams data")
    save_file = "data/teams.pkl"
    tFrame = pd.read_pickle(save_file)

    # Block off for Challenger
    cFrame.update(
        reserve_slots(
            cFrame,
            day_of_week="Sunday",
            field="Riordan",
            start="14:00",
            division="Challenger"))
    cFrame.update(
        reserve_slots(
            cFrame,
            day_of_week="Sunday",
            field="Tepper",
            start="14:00",
            division="Challenger"))

    # Remove Challenger slot on 5/11/25
    mothers_day = cFrame[cFrame["Date"] == "2025-05-11"].index
    challenger = cFrame[cFrame["Division"] == "Challenger"].index
    challenger_slots = mothers_day.intersection(challenger)
    for slot in challenger_slots:
        clear_row(cFrame, slot)

    save_frame(cFrame, "calendar.pkl")
    publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")


if __name__ == "__main__":
    # Run the main function
    main()

    # Save the frame
