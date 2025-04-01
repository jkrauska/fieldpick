import os
import time
import logging
from natsort import natsorted
from collections import defaultdict
from inputs import division_info
from helpers import short_division_names
import numpy as np
import pandas as pd
import sys

logging.basicConfig(
    format="%(asctime)s %(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger()

# helper functions for working with dataframes


def list_teams_for_division(division, tFrame):
    """Return a list of teams for a given division"""
    teams = tFrame[tFrame["Division"] == division]["Team"].tolist()
    if len(teams) < 1:
        print(f"Division {division} has no teams")
        sys.exit(1)
    print(f"Teams: ({len(teams)} - {teams}")

    return teams


def weeks_in_season(cFrame):
    """Return a list of weeks in the season"""
    weekList = cFrame["Week_Number"].unique().tolist()
    return remove_unknowns(weekList)


def remove_unknowns(mylist):
    """Remove "UNKNOWN" from a list"""
    return [i for i in mylist if i != "UNKNOWN"]


# Make sure we have a data dir
def make_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")


def load_frame(save_file):
    logger.info(f"Loading frame from {save_file}")
    myFrame = pd.read_pickle(save_file)
    print(f"Loaded {len(myFrame)} slots")
    return myFrame


def save_frame(frame, save_file):
    """Save a dataframe to a pickle file"""
    if not os.path.exists("data"):
        os.makedirs("data")

    file_path = f"data/{save_file}"

    # Check if the file exists and read it
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_content = pd.read_pickle(file_path)
    else:
        existing_content = None

    if existing_content is not None and existing_content.equals(frame):
        logger.info(f"Skipping save of {file_path} - no changes")
        return
    else:
        logger.info(f"Saving {len(frame)} rows to disk: {file_path}")
        frame.to_pickle(f"{file_path}")

        # backup
        time_str = time.strftime("%Y%m%d-%H%M%S")
        frame.to_pickle(f"{file_path}_{time_str}")


def score_frame(frame, division, column):
    """Evaluate a column in a dataframe and return a score"""

    list_of_deviations = []

    logger.info(f"Scoring {division} slots based on {column}")

    slots_to_score = filter_by_division(frame, division)
    logger.info(f"Scoring {len(slots_to_score)} slots")

    if len(slots_to_score) == 0:
        return 0

    all_teams = extract_teams(slots_to_score)

    variations = defaultdict(list)

    # count the number of times each value appears for each team
    for team in all_teams:
        matching_slots = rows_with_team(slots_to_score, team)
        value_counts = matching_slots[column].value_counts()
        for value in value_counts.index:
            variations[value].append(value_counts[value])

    for field in variations:
        dev = np.std(variations[field])
        list_of_deviations.append(dev)
        logger.debug(
            f"SCORE Field: {field} -- {variations[field]} deviation: {dev:.2f}")

    return np.mean(list_of_deviations)


def rows_with_team(frame, team):
    """Return a dataframe with rows that match a team"""
    return frame[(frame["Home_Team"] == team) | (frame["Away_Team"] == team)]


def rows_unused(frame):
    """Return a dataframe with rows that are unused"""
    return frame.query("Division != Division")


def score_frame_home(frame, division):
    """Evaluate a column in a dataframe and return a score"""

    logger.info(f"Scoring {division} slots")

    slots_to_score = filter_by_division(frame, division)
    logger.info(f"Scoring {len(slots_to_score)} slots")
    all_teams = extract_teams(slots_to_score)

    for team in all_teams:
        print(f"Team: {team}")
        home_slots = slots_to_score[slots_to_score["Home_Team"] == team]
        print(f"Home slots: {len(home_slots)}")

    print(slots_to_score)


def extract_teams(frame):
    """Extract a unique list of teams from a calendar dataframe"""
    all_teams = frame["Home_Team"].to_list()
    all_teams += frame["Away_Team"].to_list()
    all_teams = natsorted(list(set(all_teams)))
    return all_teams


def extract_divisions(frame):
    """Extract a unique list of divisions from a calendar dataframe"""
    return frame["Division"].unique().tolist()


def extract_day_of_week(frame):
    """Extract a unique list of days of the week from a calendar dataframe"""
    return frame["Day_of_Week"].unique().tolist()


def extract_field_names(frame):
    """Extract a unique list of days of the week from a calendar dataframe"""
    return frame["Full_Field"].unique().tolist()


def filter_by_division(frame, division):
    """Filter a dataframe to a specific division"""
    return frame[frame["Division"] == division]


def clear_division(frame, division):
    """Clear a division from a calendar dataframe"""
    logger.info(f"Clearing division {division}")
    frame.loc[frame["Division"] == division, "Home_Team"] = None
    frame.loc[frame["Division"] == division, "Away_Team"] = None
    frame.loc[frame["Division"] == division, "Game_ID"] = None
    frame.loc[frame["Division"] == division, "Division"] = None

    return frame


def score_gamecount(frame, division):
    variations = []
    # logger.info(f"Division: {division}")
    division_frame = filter_by_division(frame, division)
    all_teams = extract_teams(division_frame)

    for team in all_teams:
        team_frame = rows_with_team(division_frame, team)
        variations.append(len(team_frame))

    dev = np.std(variations)
    return dev * 3.0  # scale up the deviation


def sum_versus(team_frame, versus):
    home_and_away = [team_frame["Home_Team"], team_frame["Away_Team"]]
    return sum(col.astype(str).str.contains(versus).sum()
               for col in home_and_away)


# division	team	Monday	Tuesday	Wednesday	Thursday	Friday	Saturday	Sunday
# total	home	away	turf	grass
# TI	SF	M-F-TI	SS-TI	M-F-SF	SS-SF
# Tepper	Ketcham	Ft. Scott	Kimbell	SouthSunset	Paul Goode	Tepper Home	Tepper Away
# Week 1	Week 2	Week 3	Week 4	Week 5	Week 6	Week 7	Week 8	Week 9	Week 10	Week 11	Week 12	Week 13	Week 14	Week 15
# vs Team 01	vs Team 02	vs Team 03	vs Team 04	vs Team 05	vs Team 06	vs Team 07	vs Team 08	vs Team 09	vs Team 10	vs Team 11	vs Team 12	vs Team 13	vs Team 14
# vs RESERVED_
def analyze_columns(cFrame):
    output = pd.DataFrame()

    """Analyze the columns of a calendar dataframe"""
    logger.info("Analyzing columns")
    divisions = list(division_info.keys()) + \
        ["UNUSED - W1-9", "TOTALS - W1-W9", "UNUSED - ALL", "TOTALS"]
    for division in divisions:
        # logger.info(f"Division: {division}")
        if division == "UNUSED - W1-9":
            cleanFrame = cFrame[cFrame["Week_Number"] != "UNKNOWN"].copy()
            division_frame = rows_unused(cleanFrame)
            division_frame[pd.to_numeric(division_frame["Week_Number"]) < 10]
            all_teams = ["UNUSED"]
        elif division == "UNUSED - ALL":
            division_frame = rows_unused(cFrame)
            all_teams = ["UNUSED"]
        elif division == "TOTALS - W1-W9":
            division_frame = cFrame
            all_teams = ["TOTALS"]
        elif division == "TOTALS":
            division_frame = cFrame
            all_teams = ["TOTALS"]
        else:
            division_frame = filter_by_division(cFrame, division)
            all_teams = extract_teams(division_frame)

        for team in all_teams:
            # logger.info(f"Team: {team}")
            if division == "UNUSED - W1-9":
                cleanFrame = cFrame[cFrame["Week_Number"] != "UNKNOWN"].copy()
                division_frame = rows_unused(cleanFrame)
                division_frame = division_frame[pd.to_numeric(
                    division_frame["Week_Number"]) < 10]
                team_frame = division_frame
            elif division == "UNUSED - ALL":
                division_frame = rows_unused(cFrame)
                team_frame = division_frame
            elif division == "TOTALS - W1-W9":
                cleanFrame = cFrame[cFrame["Week_Number"] != "UNKNOWN"].copy()
                division_frame = cleanFrame
                division_frame = division_frame[pd.to_numeric(
                    division_frame["Week_Number"]) < 10]
                team_frame = division_frame

            elif division == "TOTALS":
                team_frame = cFrame
            else:
                team_frame = rows_with_team(division_frame, team)

            mydata = {
                "Division": division,
                "Team": team,
                "Total Games": len(team_frame),
                "Saturday": len(team_frame[team_frame["Day_of_Week"] == "Saturday"]),
                "Sunday": len(team_frame[team_frame["Day_of_Week"] == "Sunday"]),
                "Monday": len(team_frame[team_frame["Day_of_Week"] == "Monday"]),
                "Tuesday": len(team_frame[team_frame["Day_of_Week"] == "Tuesday"]),
                "Wednesday": len(team_frame[team_frame["Day_of_Week"] == "Wednesday"]),
                "Thursday": len(team_frame[team_frame["Day_of_Week"] == "Thursday"]),
                "Friday": len(team_frame[team_frame["Day_of_Week"] == "Friday"]),
                "Week 1 - Opening": len(team_frame[team_frame["Week_Name"] == "Week 1"]),
                "Week 2": len(team_frame[team_frame["Week_Name"] == "Week 2"]),
                "Week 3": len(team_frame[team_frame["Week_Name"] == "Week 3"]),
                "Week 4": len(team_frame[team_frame["Week_Name"] == "Week 4"]),
                "Week 5": len(team_frame[team_frame["Week_Name"] == "Week 5"]),
                "Week 6 - Giants": len(team_frame[team_frame["Week_Name"] == "Week 6"]),
                "Week 7": len(team_frame[team_frame["Week_Name"] == "Week 7"]),
                "Week 8 - Easter": len(team_frame[team_frame["Week_Name"] == "Week 8"]),
                "Week 9": len(team_frame[team_frame["Week_Name"] == "Week 9"]),
                "Week 10": len(team_frame[team_frame["Week_Name"] == "Week 10"]),
                "Week 11": len(team_frame[team_frame["Week_Name"] == "Week 11"]),
                "Week 12": len(team_frame[team_frame["Week_Name"] == "Week 12"]),
                "Week 13": len(team_frame[team_frame["Week_Name"] == "Week 13"]),
                "Week 14": len(team_frame[team_frame["Week_Name"] == "Week 14"]),
                "home": len(team_frame[team_frame["Home_Team"] == team]),
                "away": len(team_frame[team_frame["Away_Team"] == team]),
                "Vs 01": sum_versus(team_frame, "_01"),
                "Vs 02": sum_versus(team_frame, "_02"),
                "Vs 03": sum_versus(team_frame, "_03"),
                "Vs 04": sum_versus(team_frame, "_04"),
                "Vs 05": sum_versus(team_frame, "_05"),
                "Vs 06": sum_versus(team_frame, "_06"),
                "Vs 07": sum_versus(team_frame, "_07"),
                "Vs 08": sum_versus(team_frame, "_08"),
                "Vs 09": sum_versus(team_frame, "_09"),
                "Vs 10": sum_versus(team_frame, "_10"),
                "Vs 11": sum_versus(team_frame, "_11"),
                "Vs 12": sum_versus(team_frame, "_12"),
                "Vs 13": sum_versus(team_frame, "_13"),
                "Vs 14": sum_versus(team_frame, "_14"),
                "TI": len(team_frame[team_frame["Region"] == "TI"]),
                "SF": len(team_frame[team_frame["Region"] == "SF"]),
            }

            mydata["WeekEND"] = len(team_frame.query(
                "Day_of_Week in ('Saturday', 'Sunday')"))
            mydata["WeekDAY"] = len(team_frame.query(
                "Day_of_Week not in ('Saturday', 'Sunday')"))

            mydata["TI WeekEND"] = len(team_frame.query(
                "Region == 'TI' and Day_of_Week in ('Saturday', 'Sunday')"))
            mydata["TI WeekDAY"] = len(team_frame.query(
                "Region == 'TI' and Day_of_Week not in ('Saturday', 'Sunday')"))

            mydata["SF WeekEND"] = len(team_frame.query(
                "Region == 'SF' and Day_of_Week in ('Saturday', 'Sunday')"))
            mydata["SF WeekDAY"] = len(team_frame.query(
                "Region == 'SF' and Day_of_Week not in ('Saturday', 'Sunday')"))
            mydata["Early Starts"] = len(team_frame.query(
                "Start in ('08:00', '08:30', '09:00', '09:30')"))

            all_fields = sorted(extract_field_names(cFrame))

            # Manually tweak order
            friendly_order = [
                "Paul Goode - Practice",
                "Larsen - Field 1",
                "Fort Scott - South Diamond",
                "Fort Scott - North Diamond",
                "Laurel Hill - Field 1",
                "Kimbell - Diamond 3",
                "Kimbell - Diamond 2",
                "Kimbell - Diamond 1",
                "Tepper - Field 1",
                "Ketcham - Field 1",
                "West Sunset - Field 3"

            ]

            friendly_order.reverse()
            seen_fields = []
            for field in friendly_order:
                if field in all_fields:
                    all_fields.remove(field)
                    all_fields.insert(0, field)
                else:
                    seen_fields.append(field)
                    if field not in seen_fields:
                        logger.warning(f"Field {field} not found")
                        seen_fields.append(field)

            # Place at end
            for field in [
                "Balboa - Sweeney",
                "McCoppin",
                "Paul Goode Main",
                    "Riordan"]:
                if field in all_fields:
                    all_fields.remove(field)
                    all_fields.append(field)

            for field in all_fields:
                try:
                    mydata[field] = len(
                        team_frame[team_frame["Full_Field"] == field])
                except KeyError:
                    # logger.info(f"Field {field} not found")
                    mydata[field] = 0

            mydf = pd.DataFrame(mydata, index=[0])
            output = pd.concat(
                [output, mydf], ignore_index=True)  # concat times
    return output


def generate_schedules(cFrame):
    """Analyze the columns of a calendar dataframe"""
    division_frames = {}
    logger.info("Generating schedules")
    for division in extract_divisions(cFrame):

        # logger.info(f"Division: {division}")
        if not division:
            continue
        division_frame = filter_by_division(cFrame, division)
        all_teams = extract_teams(division_frame)
        team_frames = []
        for team in all_teams:
            # logger.info(f"Team: {team}")

            tf = cFrame.query(
                f"Division == '{division}' and (Home_Team == '{team}' or Away_Team == '{team}')")

            team_frames.append(tf)

            # Split out layout for formatting...
            empty_frame = pd.DataFrame(
                columns=[
                    "Home_Team",
                    "Away_Team",
                    "Division",]
            )

            empty_frame["Home_Team"] = "JOELTEST"
            empty_frame["Away_Team"] = team
            empty_frame["Division"] = division

            team_frames.append(empty_frame)

        division_frames[division] = pd.concat(team_frames, ignore_index=True)

    return division_frames


def generate_team_schedules(cFrame, output="frame"):
    """Analyze the columns of a calendar dataframe"""
    division_frames = defaultdict(dict)
    logger.info("Generating schedules")
    for division in extract_divisions(cFrame):

        # logger.info(f"Division: {division}")
        if not division:
            continue
        division_frame = filter_by_division(cFrame, division)
        all_teams = extract_teams(division_frame)
        team_frames = []
        for team in all_teams:

            tf = cFrame.query(
                f"Division == '{division}' and (Home_Team == '{team}' or Away_Team == '{team}')")

            division_frames[division][team] = tf

    return division_frames


def reserve_slots(
        frame,
        day_of_week=None,
        date=None,
        field=None,
        start=None,
        end=None,
        division=None,
        home_team=None,
        away_team=None):
    """Reserve slots for a given day,field, and time"""
    logger.info(f"Reserving  slots for {division}")

    frame = frame.copy()

    if day_of_week:
        frame = frame.query(f"Day_of_Week == '{day_of_week}'")
    if date:
        frame = frame.query(f"Date == '{date}'")
    if field:
        frame = frame.query(f"Field == '{field}'")
    if start:
        frame = frame.query(f"Start == '{start}'")
    if end:
        frame = frame.query(f"End == '{end}'")

    if division and not all([home_team, away_team]):
        home_team = division
        away_team = division

    frame = frame.assign(Division=division)
    frame = frame.assign(Home_Team=home_team)
    frame = frame.assign(Away_Team=away_team)

    if len(frame) == 0:
        logger.warning("No matching slots found for reservation request")
    return frame


def check_three_six(frame, division, size=6):
    """Check if there are 3 games in Y days for any given team in a given division"""
    division_frame = filter_by_division(frame, division)
    all_teams = extract_teams(division_frame)
    result = 0

    for team in all_teams:
        team_frame = rows_with_team(division_frame, team)
        day_series = team_frame.Day_of_Year.values.astype(int)
        day_series.sort()

        for i in range(len(day_series) - 2):
            spread = abs(day_series[i + 2] - day_series[i]) + 1
            if spread < size + 1:
                print(
                    f"Division: {division} \tTeam: {team}\t: Found three games in {spread} days:   {day_series[i]}-{day_series[i + 1]}-{day_series[i + 2]}")
    return result


def check_consecutive(frame, division, min_diff=2):
    """Check if there are any consecutive games for any given team in a given division"""
    # FIXME, this function slows the scoring down by 50%!  Need to do this
    # faster..
    division_frame = filter_by_division(frame, division)
    all_teams = extract_teams(division_frame)

    result = 0

    for team in all_teams:
        team_frame = rows_with_team(division_frame, team)

        day_series = team_frame.Day_of_Year.values.astype(int)

        day_series.sort()

        for i in range(len(day_series) - 1):
            diff = abs(day_series[i] - day_series[i + 1])

            # early exit if we find a diff of 1 (speedup?)
            if diff < 1:
                logger.info(
                    f"{division} {team} Found same day games. ({diff}) week {
                        i + 1} No go.")
                result += 100
            elif diff < 2:
                logger.info(
                    f"{division} {team} Found back to back consecutive games. ({diff}) week {
                        i +
                        1}  and week {
                        i +
                        2} No go.   days {
                        day_series[i]} and {
                        day_series[
                            i +
                            1]}")
                result += 10

    return result


def swap_rows_by_slot(frame, slot1, slot2, safe=True):
    if frame.loc[slot1, "Game_ID"] is None and safe:
        logger.warning(
            f"Cannot Swap - Slot {slot1} does not have a game assigned")
        return
    elif frame.loc[slot2, "Game_ID"] is None and safe:
        logger.warning(
            f"Cannot Swap Slot {slot2} does not have a game assigned")
        return
    else:
        logger.info(f"Swapping slots {slot1} and {slot2}")

        temp = frame.loc[slot1].copy()

        frame.loc[slot1, [
            "Division",
            "Home_Team", "Home_Team_Name",
            "Away_Team", "Away_Team_Name",
            "Game_ID",
            "Notes"]] = [
            frame.loc[slot2, "Division"],
            frame.loc[slot2, "Home_Team"],
            frame.loc[slot2, "Home_Team_Name"],
            frame.loc[slot2, "Away_Team"],
            frame.loc[slot2, "Away_Team_Name"],
            frame.loc[slot2, "Game_ID"],
            f"Swapped with {slot2}."
        ]

        frame.loc[slot2, [
            "Division",
            "Home_Team", "Home_Team_Name",
            "Away_Team", "Away_Team_Name", "Game_ID",
            "Notes"]] = [
            temp.Division,
            temp.Home_Team,
            temp.Home_Team_Name,
            temp.Away_Team,
            temp.Away_Team_Name,
            temp.Game_ID,
            f"Swapped with {slot1}."
        ]


def game_id_to_slot(frame, game_id):
    return frame[frame["Game_ID"] == game_id].index[0]


def swap_rows_by_game_id(frame, game_id1, game_id2, dest=None):
    slot1 = game_id_to_slot(frame, game_id1)
    slot2 = game_id_to_slot(frame, game_id2)

    if dest:
        # check if dst slot already has an expected team (swap already done)
        if frame.loc[slot2,
                     "Home_Team"] == dest or frame.loc[slot2,
                                                       "Away_Team"] == dest:
            logger.info(
                f"Not swapping rows -- Slot {slot2} already has {dest} assigned")
            return
    swap_rows_by_slot(frame, slot1, slot2)


def balance_home_away(frame):
    """Balance home and away games"""
    for division in extract_divisions(frame):
        # logger.info(f"Division: {division}")
        if not division:
            continue

        # if division != "Tee Ball": continue  # Only balance Tee Ball

        division_frame = filter_by_division(frame, division)

        home = division_frame["Home_Team"]
        home_counts = home.value_counts()
        home_dev = home_counts.astype(float).std()
        top_home = next(iter(home_counts.to_dict()))

        if home_dev < 0.3:
            # logger.info(f"Deviation: {home_dev} - skipping")
            continue

        away = division_frame["Away_Team"]
        away_counts = away.value_counts()
        away_counts.astype(float).std()

        away_counts_dict = list(away_counts.to_dict().keys())

        if len(away_counts_dict) < 2:
            # logger.info("not enough away teams to flip - skipping")
            continue

        for check_team in away_counts_dict:
            possible_flip = division_frame.query(
                f"Home_Team == '{top_home}' and Away_Team == '{check_team}'")
            if len(possible_flip) == 0:
                # logger.info(f"No faceoff found between home: {top_home} and away: {check_team}")
                continue
            else:
                flip_index = possible_flip.index[0]
                # logger.info(f"Match between home:{top_home} and away:{check_team} found - flipping")
                flip_away = check_team
                break

        frame.loc[flip_index, [
            "Home_Team", "Home_Team_Name",
            "Away_Team", "Away_Team_Name"]] = [
                flip_away, flip_away,
                top_home, top_home]


def assign_row(frame, slot, division, home_team, away_team, safe=True):

    # logger.info(f"Assigning {division} {home_team} vs {away_team} to slot {slot}")

    # Get the next available id
    game_ids = frame[frame['Game_ID'].notnull()]["Game_ID"].astype(
        str).str.split("-").str[1].astype(int)
    game_id = game_ids.max() + 1 if len(game_ids) > 0 else 1

    # game_id = 428

    game_id_string = f"{short_division_names[division]}-{game_id:03d}"

    if frame.loc[slot, "Game_ID"] is not None and safe:
        logger.warning(f"Slot {slot} already has a game assigned")
    else:
        # logger.info(f"Assigning {game_id_string} to slot {slot}")
        frame.loc[slot, ["Division",
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
