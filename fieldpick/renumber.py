import math
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
    cFrame.loc[slot,
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


def move_row(frame, slot, new_slot):

    if cFrame.loc[new_slot, "Game_ID"] is not None:
        logger.warning(f"Slot {new_slot} already has a game assigned")
        return
    elif cFrame.loc[slot, "Game_ID"] is None:
        logger.warning(f"Slot {slot} does not have a game assigned")
        return
    else:
        cFrame.loc[new_slot,
                   ["Division",
                    "Home_Team",
                    "Home_Team_Name",
                    "Away_Team",
                    "Away_Team_Name",
                    "Game_ID"]] = [cFrame.loc[slot,
                                              "Division"],
                                   cFrame.loc[slot,
                                              "Home_Team"],
                                   cFrame.loc[slot,
                                              "Home_Team_Name"],
                                   cFrame.loc[slot,
                                              "Away_Team"],
                                   cFrame.loc[slot,
                                              "Away_Team_Name"],
                                   cFrame.loc[slot,
                                              "Game_ID"],
                                   ]
        clear_row(frame, slot)


id = 1
for division in short_division_names:
    print(f"Renumbering {division}")

    for slot in cFrame[cFrame["Division"] == division].index:
        game_id_string = f"{short_division_names[division]}-{id:03d}"

        old_game_id = cFrame.loc[slot, "Game_ID"]

        # if old_game_id == game_id_string:
        #     continue
        # else:
        #     print
        # cFrame.loc[slot, "Old_Game_ID"] = cFrame.loc[slot, "Game_ID"]
        print(f"Renumbering {slot} from {old_game_id} to {game_id_string}")
        cFrame.loc[slot, "Game_ID"] = game_id_string

        if cFrame.loc[slot, "Notes"]:
            if "Swapped" in cFrame.loc[slot, "Notes"]:
                cFrame.loc[slot, "Notes"] = "None"

        id += 1
    id = (int(math.ceil(id / 100.0)) * 100) + 1

# cFrame.drop('GAME_ID', axis=1, inplace=True)
try:
    cFrame.drop("Old_Game_ID", axis=1, inplace=True)
except KeyError:
    pass


# Clear notes, send empty gameID
id = 1001
for slot in cFrame.index:
    if cFrame.loc[slot, "Notes"]:
        if "Swapped" in cFrame.loc[slot, "Notes"]:
            cFrame.loc[slot, "Notes"] = "None"

    if cFrame.loc[slot, "Game_ID"] is None:
        game_id_string = f"NONE-{id:03d}"

        # print(f"Numbering {slot} to {game_id_string}")
        cFrame.loc[slot, "Game_ID"] = game_id_string
        id += 1


# sys.exit(1)

save_frame(cFrame, "calendar.pkl")
publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")


aFrame = analyze_columns(cFrame)
publish_df_to_gsheet(aFrame, worksheet_name="Analysis")
