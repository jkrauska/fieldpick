import pandas as pd
import logging
from frametools import analyze_columns, swap_rows_by_game_id, balance_home_away, swap_rows_by_slot, assign_row
from gsheets import publish_df_to_gsheet
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





def clear_row(frame, slot):
    cFrame.loc[slot, ["Division", 
    "Home_Team", "Home_Team_Name", 
    "Away_Team", "Away_Team_Name", 
    "Game_ID"]] = [
        None,
        None,
        None,
        None,
        None,
        None
    ]

def move_row(frame, slot, new_slot):

    if cFrame.loc[new_slot, "Game_ID"] is not None:
        logger.warning(f"Slot {new_slot} already has a game assigned")
        return
    elif cFrame.loc[slot, "Game_ID"] is None:
        logger.warning(f"Slot {slot} does not have a game assigned")
        return
    else:
        logger.info(f"Moving game {cFrame.loc[slot, 'Game_ID']} from slot {slot} to slot {new_slot}")
        cFrame.loc[new_slot, ["Division", 
        "Home_Team", "Home_Team_Name", 
        "Away_Team", "Away_Team_Name", 
        "Game_ID"]] = [
            cFrame.loc[slot, "Division"],
            cFrame.loc[slot, "Home_Team"],
            cFrame.loc[slot, "Home_Team_Name"],
            cFrame.loc[slot, "Away_Team"],
            cFrame.loc[slot, "Away_Team_Name"],
            cFrame.loc[slot, "Game_ID"]
        ]
        clear_row(frame, slot)





## Checkpoint Friday night at 9pm

# FML-077	FML-080	2
# FML-086	FML-087	2
# FML-102	FML-105	4
# FML-107	FML-111	5
# swap_rows_by_game_id(cFrame, "FML-077", "FML-080", dest="Team 2")
# swap_rows_by_game_id(cFrame, "FML-086", "FML-087", dest="Team 2")
# swap_rows_by_game_id(cFrame, "FML-102", "FML-105", dest="Team 4")
# swap_rows_by_game_id(cFrame, "FML-107", "FML-111", dest="Team 5")



# RK-682 with RK-684
# RK-683 with RK-685
# RK-689 with RK-703
# swap_rows_by_game_id(cFrame, "RK-682", "RK-684", dest="Team 13")
# swap_rows_by_game_id(cFrame, "RK-683", "RK-685", dest="Team 2")
# swap_rows_by_game_id(cFrame, "RK-689", "RK-703", dest="Team 4")



# TB-016	TB-017	2
# TB-053	TB-054	2
# FML-143	FML-147	2
# FML-108	FML-112	4
# FML-102	FML-106	3
# swap_rows_by_game_id(cFrame, "TB-016", "TB-017", dest="Team 2")
# swap_rows_by_game_id(cFrame, "TB-053", "TB-054", dest="Team 2")
# swap_rows_by_game_id(cFrame, "FML-143", "FML-147", dest="Team 2")
# swap_rows_by_game_id(cFrame, "FML-108", "FML-112", dest="Team 4")
# swap_rows_by_game_id(cFrame, "FML-102", "FML-106", dest="Team 3")


# TB-002	TB-007	10
# swap_rows_by_game_id(cFrame, "TB-002", "TB-007", dest="Team 10")

# FMU-222	2023-03-26	11:30	14:00	150	2023-03-26 11:30:00	85	Tepper
# FMU-223	2023-03-26	13:00	15:30	150	2023-03-26 13:00:00	85	Rossi Park #1
# FMU-271	2023-05-21	13:00	15:30	150	2023-05-21 13:00:00	141	Rossi Park #1
# FMU-272	2023-05-21	15:30	18:00	150	2023-05-21 15:30:00	141	Rossi Park #1


# # FMU-222	2023-03-26	11:30	14:00	150	2023-03-26 11:30:00	85	Tepper
# 181 to 207

# FMU-223	2023-03-26	13:00	15:30	150	2023-03-26 13:00:00	85	Rossi Park #1
# # 188 to 210
# move_row(cFrame, 188, 210)

# # FMU-271	2023-05-21	13:00	15:30	150	2023-05-21 13:00:00	141	Rossi Park #1
# # 598 to 620
# move_row(cFrame, 598, 620)


# # # FMU-272	2023-05-21	15:30	18:00	150	2023-05-21 15:30:00	141	Rossi Park #1
# # 603 to 609
# move_row(cFrame, 603, 609)


# fix 609 to 625
# move_row(cFrame, 609, 625)

# Swaps
# RK-301	RK-303 Team 8
# RK-371	RK-373 Team 14
# swap_rows_by_game_id(cFrame, "RK-301", "RK-303", dest="Team 8")
#swap_rows_by_game_id(cFrame, "RK-371", "RK-373", dest="Team 14")


# swap_rows_by_game_id(cFrame, "FML-107", "FML-111", dest="Team 5")


# AAA-523	AA-428
# swap_rows_by_game_id(cFrame, "AAA-523", "AA-428", dest="Team 3")


#cFrame.sort_values(by=["Datestamp"], inplace=True, ignore_index=True)
def move_row(frame, slot, new_slot):

    logger.info(f"Moving row {slot} to {new_slot}")
    if cFrame.loc[new_slot, "Game_ID"] is not None and cFrame.loc[new_slot, "Division"] is not None:
        logger.warning(f"Slot {new_slot} already has a game assigned")
        return
    elif cFrame.loc[slot, "Game_ID"] is None:
        logger.warning(f"Slot {slot} does not have a game assigned")
        return
    else:
        cFrame.loc[new_slot, ["Division", "Home_Team", "Home_Team_Name", "Away_Team", "Away_Team_Name", "Game_ID"]] = [
            cFrame.loc[slot, "Division"],
            cFrame.loc[slot, "Home_Team"],
            cFrame.loc[slot, "Home_Team_Name"],
            cFrame.loc[slot, "Away_Team"],
            cFrame.loc[slot, "Away_Team_Name"],
            cFrame.loc[slot, "Game_ID"],
        ]
        clear_row(frame, slot)

# move_row(cFrame, 86, 743)
# move_row(cFrame, 225, 226)

# #



# AAA-534	MAJ-652
#swap_rows_by_game_id(cFrame, "AAA-534", "MAJ-652", dest="Team 7")

# AA-404    AA-405
# swap_rows_by_game_id(cFrame, "AA-404", "AA-405", dest="Team 3")

# move 394, 384
# move_row(cFrame, 394, 384)



# FMU-222 and RK-326  get FMU to Sat only
#swap_rows_by_game_id(cFrame, "FMU-222", "RK-326", dest="Team 2")

cFrame.loc[185, "End"] = "12:00"
cFrame.loc[185, "Time_Length"] = 150



save_frame(cFrame, "calendar.pkl")
publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")


aFrame = analyze_columns(cFrame)
publish_df_to_gsheet(aFrame, worksheet_name="Analysis")