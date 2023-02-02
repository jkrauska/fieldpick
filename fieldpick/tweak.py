import pandas as pd
import logging
from frametools import filter_by_division, extract_divisions, analyze_columns
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





def assign_row(frame, slot, division, home_team, away_team, safe=True):


    # Get the next available id
    game_ids = frame[frame['Game_ID'].notnull()]["Game_ID"].astype(str).str.split("-").str[1].astype(int)
    game_id = game_ids.max() + 1

    #game_id = 428

    game_id_string = f"{short_division_names[division]}-{game_id:03d}"


    if cFrame.loc[slot, "Game_ID"] is not None and safe:
        logger.warning(f"Slot {slot} already has a game assigned")
    else:
        logger.info(f"Assigning {game_id_string} to slot {slot}")
        cFrame.loc[slot, ["Division", 
        "Home_Team", "Home_Team_Name", 
        "Away_Team", "Away_Team_Name", 
        "Game_ID"]] = [
            division,
            home_team,
            home_team,
            away_team,
            away_team,
            game_id_string
        ]

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


# Manual Fixes
##  Rookie
assign_row(cFrame, 106, "Rookie", "Team 6", "Team 7")
assign_row(cFrame, 437, "Rookie", "Team 3", "Team 7")
assign_row(cFrame, 289, "Rookie", "Team 9", "Team 5")
assign_row(cFrame, 378, "Rookie", "Team 3", "Team 10")
assign_row(cFrame, 110, "Rookie", "Team 3", "Team 11")
assign_row(cFrame, 112, "Rookie", "Team 1", "Team 13")
assign_row(cFrame, 443, "Rookie", "Team 9", "Team 4")
assign_row(cFrame, 504, "Rookie", "Team 12", "Team 11")
assign_row(cFrame, 308, "Rookie", "Team 9", "Team 10")
assign_row(cFrame, 227, "Rookie", "Team 3", "Team 14")

# override to balance
assign_row(cFrame, 418, "Rookie", "Team 7", "Team 2")

## AA
assign_row(cFrame,  492, "Minors AA", "Team 8", "Team 7")
assign_row(cFrame,  310, "Minors AA", "Team 10", "Team 5")
assign_row(cFrame,  162, "Minors AA", "Team 10", "Team 9")



## AAA 
assign_row(cFrame,  20, "Minors AAA", "Team 8", "Team 5")
assign_row(cFrame,  37, "Minors AAA", "Team 5", "Team 1")
assign_row(cFrame,  103, "Minors AAA", "Team 7", "Team 4")

assign_row(cFrame,  166, "Minors AAA", "Team 3", "Team 2")
#move_row(cFrame,  170,  173)

#move_row(cFrame,  459,  445)

## Majors
logger.info("Fixing Majors")
assign_row(cFrame,  235, "Majors", "Team 10", "Team 2")
assign_row(cFrame,  287, "Majors", "Team 1", "Team 6")


#sys.exit(0)

def balance_home_away(frame):
    """Balance home and away games"""
    for division in extract_divisions(frame):
        #logger.info(f"Division: {division}")
        if not division: continue

        #if division != "Tee Ball": continue  # Only balance Tee Ball

        division_frame = filter_by_division(frame, division)

        home = division_frame["Home_Team"]
        home_counts = home.value_counts()
        home_dev = home_counts.astype(float).std()
        top_home = next(iter(home_counts.to_dict()))


        if home_dev < 0.3:
            #logger.info(f"Deviation: {home_dev} - skipping")
            continue
 
        away = division_frame["Away_Team"]
        away_counts = away.value_counts()
        away_counts.astype(float).std()

        away_counts_dict = list(away_counts.to_dict().keys())

        if len(away_counts_dict) < 2:
            #logger.info("not enough away teams to flip - skipping")
            continue

        for check_team in away_counts_dict:
            possible_flip = division_frame.query(f"Home_Team == '{top_home}' and Away_Team == '{check_team}'")
            if len(possible_flip) == 0:
                #logger.info(f"No faceoff found between home: {top_home} and away: {check_team}")
                continue
            else:
                flip_index = possible_flip.index[0]
                #logger.info(f"Match between home:{top_home} and away:{check_team} found - flipping")
                flip_away = check_team
                break

        frame.loc[flip_index, [
            "Home_Team", "Home_Team_Name", 
            "Away_Team", "Away_Team_Name"]] = [
                flip_away, flip_away, 
                top_home, top_home]


    
for i in range(100):
    #logger.info('*'*80) 
    balance_home_away(cFrame)


save_frame(cFrame, "calendar.pkl")
publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")


aFrame = analyze_columns(cFrame)
publish_df_to_gsheet(aFrame, worksheet_name="Analysis")