import pandas as pd
import logging
import warnings
from frametools import (
    analyze_columns,
    balance_home_away,
    assign_row,
    clear_division,
    save_frame,
    reserve_slots,
)
from gsheets import publish_df_to_gsheet
from helpers import short_division_names
from inputs import division_info
import re
from pulp import *
from collections import Counter

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

# Load division data
logger.info("Loading teams data")
save_file = "data/teams.pkl"
tFrame = pd.read_pickle(save_file)


############################################################################################################
### PULP STUFF


# Data cleanup
cleanFrame = cFrame[cFrame["Week_Number"] != "UNKNOWN"].copy()


# Working Slots
correct_time = (cleanFrame["Time_Length"] == "150") & (pd.isna(cleanFrame["Week_Number"]) == False)
non_blocked = cleanFrame["Notes"] != "Opening Day Ceremony"
less_than_10 = pd.to_numeric(cleanFrame["Week_Number"]) < 10
not_upper_farm = cleanFrame["Division"] != "Upper Farm"  # UF has a few 150 games
not_challenger = cleanFrame["Division"] != "Challenger"  # UF has a few 150 games


slot_mask = correct_time & non_blocked & not_upper_farm & less_than_10 & not_challenger

working_slots = cleanFrame[slot_mask]

print(f"Usable Slots: {len(working_slots)}")


# Extract series we need from working_slots
days_of_week = working_slots["Day_of_Week"].unique()
days_of_year = working_slots["Day_of_Year"].unique()
weeks = working_slots["Week_Name"].unique()
fields = working_slots["Field"].unique()

# Extract Divisions
divisions = list(tFrame["Division"].unique())
# Remove non-150 divisions
for non150 in ["Tee Ball", "Upper Farm", "Lower Farm", "Challenger", "Juniors"]:
    try:
        divisions.remove(non150)
    except:
        pass

# Remove all division data
for division in divisions:
    clear_division(cFrame, division)

print(f"Divisions: {divisions}")


############################################################################################################
# Slot Variables
slots = working_slots.index

# Helpful Dict of each division's teams
teams_by_division = {}
for division in divisions:
    teams_by_division[division] = tFrame[tFrame["Division"] == division]["Team"].unique()


# Create every combination of slot, home team, away team as a LPvariable dict
# warnings.warn("Spaces are not permitted in the name. Converted to '_'")
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    slots_vars = pulp.LpVariable.dicts(
        "Slot",
        [
            (slot, division, home, away)
            for slot in slots
            for division in divisions
            for home in teams_by_division[division]
            for away in teams_by_division[division]
        ],
        cat="Binary",
    )

############################################################################################################
prob = LpProblem("League scheduling", LpMinimize)

############################################################################################################
# objective minimize games played
prob += lpSum([slots_vars]), "Number of games played should be minimized"  # Odd objective function?


############################################################################################################

# Set rigid games per team
for division in divisions:
    games_per_team = division_info[division]["games"]
    teams = teams_by_division[division]
    for j in teams:
        prob += (
            lpSum([slots_vars[i, division, j, k] for i in slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in slots for k in teams])
        ) == games_per_team, f"Games_per_team_{division}_{j}"

# Only allow one game per slot
for i in slots:
    prob += (
        lpSum(
            [
                slots_vars[i, division, home, away]
                for division in divisions
                for home in teams_by_division[division]
                for away in teams_by_division[division]
            ]
        )
        <= 1,
        f"Only_one_game_per_slot_{i}",
    )

# No team can play itself
for division in divisions:
    teams = teams_by_division[division]
    for i in slots:
        prob += (
            lpSum([slots_vars[i, division, j, k] for j in teams for k in teams if j == k]) == 0,
            f"No_Same_Team_{division}_{i}",
        )

# All teams must play each other at least once
for division in divisions:
    if division == "Rookie":  # Rookie cannot play all..
        continue
    teams = teams_by_division[division]
    for j in teams:
        for k in teams:
            if j != k:
                prob += (
                    lpSum([slots_vars[i, division, j, k] for i in slots]) + lpSum([slots_vars[i, division, k, j] for i in slots])
                ) >= 1, f"Min_games_per_pair_{division}_{j}_{k}"

# No team should play the same team more than twice
for division in divisions:
    teams = teams_by_division[division]
    for j in teams:
        for k in teams:
            if j != k:
                prob += (
                    lpSum([slots_vars[i, division, j, k] for i in slots]) + lpSum([slots_vars[i, division, k, j] for i in slots])
                ) <= 2, f"Max_games_per_pair_{division}_{j}_{k}"

# No Rookie team should play the same team more than once
for division in ["Rookie"]:
    teams = teams_by_division[division]
    for j in teams:
        for k in teams:
            if j != k:
                prob += (
                    lpSum([slots_vars[i, division, j, k] for i in slots]) + lpSum([slots_vars[i, division, k, j] for i in slots])
                ) <= 1, f"Max_ROOKIE_games_per_pair_{division}_{j}_{k}"

# No team should play more than 2 games per week
for week in weeks:
    this_week = working_slots[working_slots["Week_Name"] == week].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                (
                    lpSum([slots_vars[i, division, j, k] for i in this_week for k in teams])
                    + lpSum(
                        [slots_vars[i, division, k, j] for i in this_week for k in teams]
                    )  # home team on week  # away team on week
                )
                <= 2,
                f"Max_two_games_per_week_{division}_{week}_team_{j}",
            )

# Min one week except for W1 and W6

for week in weeks:
    if week in ["Week 1", "Week 6"]:
        continue
    this_week = working_slots[working_slots["Week_Name"] == week].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                (
                    lpSum([slots_vars[i, division, j, k] for i in this_week for k in teams])
                    + lpSum(
                        [slots_vars[i, division, k, j] for i in this_week for k in teams]
                    )  # home team on week  # away team on week
                )
                >= 1,
                f"Min_one_games_per_week_{division}_{week}_team_{j}",
            )


# No team can play more than 1 game per day
for day in days_of_year:
    this_day = working_slots[working_slots["Day_of_Year"] == day].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                (
                    lpSum([slots_vars[i, division, j, k] for i in this_day for k in teams])
                    + lpSum(
                        [slots_vars[i, division, k, j] for i in this_day for k in teams]
                    )  # home team on day  # away team on day
                )
                <= 1,
                f"Max_games_per_day_{division}_{day}_team_{j}",
            )

# Set team days off
for division in divisions:
    day_off = division_info[division]["day_off"]
    teams = teams_by_division[division]
    off_days = working_slots[working_slots["Day_of_Week"] == day_off].index
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in off_days for j in teams for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in off_days for j in teams for k in teams])
    ) == 0, f"Division_days_off_{division}"


# # No team can play back to back games
for day in days_of_year:
    this_day = working_slots[working_slots["Day_of_Year"] == day].index
    next_day = working_slots[working_slots["Day_of_Year"] == str(int(day) + 1)].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                (
                    lpSum([slots_vars[i, division, j, k] for i in this_day for k in teams])  # home team on day
                    + lpSum([slots_vars[i, division, k, j] for i in this_day for k in teams])  # away team on day
                    + lpSum([slots_vars[i, division, j, k] for i in next_day for k in teams])  # home team on day+1
                    + lpSum([slots_vars[i, division, k, j] for i in next_day for k in teams])  # away team on day+1
                )
                <= 1,
                f"Back_to_back_{division}_{day}_team_{j}",
            )

# No team can play 3 games in 5 days
for day in days_of_year:
    day_one = working_slots[working_slots["Day_of_Year"] == day].index
    day_two = working_slots[working_slots["Day_of_Year"] == str(int(day) + 1)].index
    day_three = working_slots[working_slots["Day_of_Year"] == str(int(day) + 2)].index
    day_four = working_slots[working_slots["Day_of_Year"] == str(int(day) + 3)].index
    day_five = working_slots[working_slots["Day_of_Year"] == str(int(day) + 4)].index
    five_days = list(day_one) + list(day_two) + list(day_three) + list(day_four) + list(day_five)
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                (
                    lpSum([slots_vars[i, division, j, k] for i in five_days for k in teams])  # home team on day
                    + lpSum([slots_vars[i, division, k, j] for i in five_days for k in teams])  # away team on day
                )
                <= 2,
                f"3_games_in_5_days_{division}_{day}_team_{j}",
            )


# # No team can should play 3 games in 6 days more than once
for day in days_of_year:
    day_one = working_slots[working_slots["Day_of_Year"] == day].index
    day_two = working_slots[working_slots["Day_of_Year"] == str(int(day) + 1)].index
    day_three = working_slots[working_slots["Day_of_Year"] == str(int(day) + 2)].index
    day_four = working_slots[working_slots["Day_of_Year"] == str(int(day) + 3)].index
    day_five = working_slots[working_slots["Day_of_Year"] == str(int(day) + 4)].index
    day_six = working_slots[working_slots["Day_of_Year"] == str(int(day) + 5)].index

    six_days = list(day_one) + list(day_two) + list(day_three) + list(day_four) + list(day_five) + list(day_six)
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                (
                    lpSum([slots_vars[i, division, j, k] for i in six_days for k in teams])  # home team on day
                    + lpSum([slots_vars[i, division, k, j] for i in six_days for k in teams])  # away team on day
                )
                <= 2,  # Not sure about this...2 or 3?
                f"3_games_in_6_days_{division}_{day}_team_{j}",
            )

# Block denied fields
for division in divisions:
    denied_fields = division_info[division].get("denied_fields", [])
    logger.info(f"{division} denied_fields: {denied_fields}")
    denied_fields_slots = working_slots[working_slots["Field"].isin(denied_fields)].index
    teams = teams_by_division[division]
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in denied_fields_slots for j in teams for k in teams])
    ) == 0, f"Denied_fields_{division}"

# Limit TI Midweek
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekday_slots = working_slots[working_slots["Day_of_Week"].isin(weekdays)].index
ti_slots = working_slots[working_slots["location"] == "TI"].index
ti_weekday_slots = list(set(ti_slots).intersection(weekday_slots))
for division in divisions:
    teams = teams_by_division[division]
    ti_weekday = division_info[division].get("ti_weekday", 9)
    for j in teams:
        prob += (
            lpSum([slots_vars[i, division, j, k] for i in ti_weekday_slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in ti_weekday_slots for k in teams])
        ) <= ti_weekday, f"Limit_TI_midweek_{division}_{j}"


# Rookie TI overall cap
ti_slots = working_slots[working_slots["location"] == "TI"].index
division = "Rookie"
teams = teams_by_division[division]
for j in teams:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in ti_slots for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in ti_slots for k in teams])
    ) == 3, f"Rookie_limit_ti_{division}_{j}"


# Only Majors weekday games in Week 1
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekday_slots = working_slots[working_slots["Day_of_Week"].isin(weekdays)].index
week1_slots = working_slots[working_slots["Week_Name"] == "Week 1"].index
week1_weekday_slots = list(set(week1_slots).intersection(weekday_slots))
for division in divisions:
    if division == "Majors":
        continue
    teams = teams_by_division[division]
    for j in teams:
        prob += (
            lpSum([slots_vars[i, division, j, k] for i in week1_weekday_slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in week1_weekday_slots for k in teams])
        ) == 0, f"Non_Majors_weekday_week1_{division}_{j}"


# Try to get 7 weekend days for Majors
weekends = ["Saturday", "Sunday"]
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(weekends)].index
for division in ["Majors"]:
    teams = teams_by_division[division]
    for j in teams:
        prob += (
            lpSum([slots_vars[i, division, j, k] for i in weekend_slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in weekend_slots for k in teams])
        ) >= 7, f"Major_weekend_days_{division}_{j}"

# No single field used more than games_per_team / 2
for field in fields:
    field_slots = working_slots[working_slots["Field"] == field].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                lpSum([slots_vars[i, division, j, k] for i in field_slots for k in teams])
                + lpSum([slots_vars[i, division, k, j] for i in field_slots for k in teams])
            ) <= int(games_per_team / 2) - 1, f"Single_field_{field}_{division}_{j}"


# Everyone SF Weekend atleast once
weekends = ["Saturday", "Sunday"]
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(weekends)].index
sf_slots = working_slots[working_slots["location"] == "SF"].index
sf_weekend_slots = list(set(sf_slots).intersection(weekend_slots))
for division in divisions:
    teams = teams_by_division[division]
    for j in teams:
        prob += (
            lpSum([slots_vars[i, division, j, k] for i in sf_weekend_slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in sf_weekend_slots for k in teams])
        ) >= 1, f"SF_Weekend_{division}_{j}"

# # Try to play Tepper atleast once
# tepper_slots = working_slots[working_slots["location"] == "Tepper"].index
# for division in divisions:
#     teams = teams_by_division[division]
#     for j in teams:
#         prob += (
#             lpSum([slots_vars[i, division, j, k] for i in tepper_slots for k in teams])
#             + lpSum([slots_vars[i, division, k, j] for i in tepper_slots for k in teams])
#         ) >= 1, f"Tepper_{division}_{j}"


# Try to balance Tepper and Ketcham
# t - k <= 2
tepper_slots = working_slots[working_slots["location"] == "Tepper"].index
ketcham_slots = working_slots[working_slots["location"] == "Ketcham"].index
for division in divisions:
    teams = teams_by_division[division]
    for j in teams:
        prob += (
            lpSum([slots_vars[i, division, j, k] for i in tepper_slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in tepper_slots for k in teams])
            - lpSum([slots_vars[i, division, j, k] for i in ketcham_slots for k in teams])
            - lpSum([slots_vars[i, division, k, j] for i in ketcham_slots for k in teams])
        ) <= 2, f"Tepper_Ketcham_{division}_{j}"
        # k - t <= 2

        prob += (
            lpSum([slots_vars[i, division, j, k] for i in ketcham_slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in ketcham_slots for k in teams])
            - lpSum([slots_vars[i, division, j, k] for i in tepper_slots for k in teams])
            - lpSum([slots_vars[i, division, k, j] for i in tepper_slots for k in teams])
        ) <= 2, f"Ketcham_Tepper_{division}_{j}"


# Try to balance Weekday and Weekend
weekday_slots = working_slots[working_slots["Day_of_Week"].isin(weekdays)].index
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(weekends)].index
for division in ["Majors"]:
    teams = teams_by_division[division]
    for j in teams:
        # wd - we <= 2

        prob += (
            lpSum([slots_vars[i, division, j, k] for i in weekday_slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in weekday_slots for k in teams])
            - lpSum([slots_vars[i, division, j, k] for i in weekend_slots for k in teams])
            - lpSum([slots_vars[i, division, k, j] for i in weekend_slots for k in teams])
        ) <= 2, f"Weekday_Weekend_{division}_{j}"

        # we - wd <= 2

        prob += (
            lpSum([slots_vars[i, division, j, k] for i in weekend_slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in weekend_slots for k in teams])
            - lpSum([slots_vars[i, division, j, k] for i in weekday_slots for k in teams])
            - lpSum([slots_vars[i, division, k, j] for i in weekday_slots for k in teams])
        ) <= 2, f"Weekend_Weekday_{division}_{j}"


# Try to balance TI and SF

ti_slots = working_slots[working_slots["location"] == "TI"].index
weekday_slots = working_slots[working_slots["Day_of_Week"].isin(weekdays)].index
ti_weekday_slots = list(set(ti_slots).intersection(weekday_slots))

sf_slots = working_slots[working_slots["location"] == "SF"].index
for division in ["Majors"]:
    teams = teams_by_division[division]
    for j in teams:
        # ti - sf <= ??

        prob += (
            lpSum([slots_vars[i, division, j, k] for i in ti_slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in ti_slots for k in teams])
            - lpSum([slots_vars[i, division, j, k] for i in sf_slots for k in teams])
            - lpSum([slots_vars[i, division, k, j] for i in sf_slots for k in teams])
        ) <= 3, f"TI_SF_{division}_{j}"

# TI Weekday > 2 for Majors
for division in ["Majors"]:
    teams = teams_by_division[division]
    for j in teams:
        prob += (
            lpSum([slots_vars[i, division, j, k] for i in ti_weekday_slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in ti_weekday_slots for k in teams])
        ) >= 2, f"TI_Weekday_MIN2{division}_{j}"


############################################################################################################
############################################################################################################

# Special asks
# Rookie

division = "Rookie"
teams = teams_by_division[division]


# Everyone atleast one sunday
sunday_slots = working_slots[working_slots["Day_of_Week"] == "Sunday"].index
for j in teams:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in sunday_slots for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in sunday_slots for k in teams])
    ) >= 1, f"Sunday_mornings_{division}_{j}"


# No Team 4 on Wednesdays
dow_slots = working_slots[working_slots["Day_of_Week"] == "Wednesday"].index
for j in ["Team 4"]:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in dow_slots for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in dow_slots for k in teams])
    ) == 0, f"No_Wednesdays_{division}_{j}"


# No Team 3 before 1pm on 3/5, 3/12, 3/19
date_list = ["2023-03-05", "2023-03-12", "2023-03-19"]
date_slots = working_slots[working_slots["Date"].isin(date_list)].index
am_times = ["9:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30"]
am_slots = working_slots[working_slots["Start"].isin(am_times)].index
date_am_slots = list(set(date_slots).intersection(am_slots))
for j in ["Team 3"]:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in date_slots for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in date_slots for k in teams])
    ) == 0, f"No_3_5_3_12_3_19_AM_{division}_{j}"

# No team 8 on Sunday Mornings
sunday_slots = working_slots[working_slots["Day_of_Week"] == "Sunday"].index
am_times = ["9:00", "09:30", "10:00", "10:30", "11:00", "11:30"]
am_slots = working_slots[working_slots["Start"].isin(am_times)].index
sunday_mornings = list(set(sunday_slots).intersection(am_slots))
for j in ["Team 8"]:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in sunday_mornings for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in sunday_mornings for k in teams])
    ) == 0, f"No_Sunday_mornings_{division}_{j}"

# Minimal Team 4 games between 4/26 and 4/30
date_list = ["2023-04-26", "2023-04-27", "2023-04-28", "2023-04-29", "2023-04-30"]
date_slots = working_slots[working_slots["Date"].isin(date_list)].index
for j in ["Team 4"]:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in date_slots for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in date_slots for k in teams])
    ) == 0, f"Minimal_games_4_26_4_30_{division}_{j}"


# Minimal Team 4 games between 3/20 and 3/27
date_list = ["2023-03-20", "2023-03-21", "2023-03-22", "2023-03-23", "2023-03-24", "2023-03-25", "2023-03-26", "2023-03-27"]
date_slots = working_slots[working_slots["Date"].isin(date_list)].index
for j in ["Team 4"]:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in date_slots for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in date_slots for k in teams])
    ) == 0, f"Minimal_games_3_20_3_27_{division}_{j}"
############################################################################################################

division = "Minors AAA"
teams = teams_by_division[division]


# Everyone atleast one Saturday
saturday_slots = working_slots[working_slots["Day_of_Week"] == "Saturday"].index
for j in teams:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in saturday_slots for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in saturday_slots for k in teams])
    ) >= 1, f"Saturdays_{division}_{j}"


# Atleast three SF
sf_slots = working_slots[working_slots["location"] == "SF"].index
for j in teams:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in sf_slots for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in sf_slots for k in teams])
    ) >= 3, f"SF_{division}_{j}"


############################################################################################################


division = "Majors"
teams = teams_by_division[division]

# Everyone atleast one Saturday
saturday_slots = working_slots[working_slots["Day_of_Week"] == "Saturday"].index
for j in teams:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in saturday_slots for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in saturday_slots for k in teams])
    ) >= 1, f"Saturdays_{division}_{j}"

# No Team 10 on Fridays
dow_slots = working_slots[working_slots["Day_of_Week"] == "Friday"].index
for j in ["Team 10"]:
    prob += (
        lpSum([slots_vars[i, division, j, k] for i in dow_slots for k in teams])
        + lpSum([slots_vars[i, division, k, j] for i in dow_slots for k in teams])
    ) == 0, f"No_Fridays_{division}_{j}"


# Ensure tepper Sundays at 11:30 is Majors by saying it's not any of the other divisions
bad_divisions = ["Minors AAA", "Rookie", "Minors AA"]
sunday_slots = working_slots[working_slots["Day_of_Week"] == "Sunday"].index
am_times = ["11:30"]
am_slots = working_slots[working_slots["Start"].isin(am_times)].index
fields = ["Tepper"]
field_slots = working_slots[working_slots["Field"].isin(fields)].index
sunday_before_challenger_tepper_slots = list(set(sunday_slots).intersection(am_slots).intersection(field_slots))


for slot in sunday_before_challenger_tepper_slots:
    prob += lpSum([slots_vars[slot, division, j, k] for j in teams for k in teams]) == 1, f"Tepper_Sunday_1130_{division}_{slot}"


############################################################################################################
############################################################################################################
# Double Division Coaches!

# James Baird
team1 = ("Minors AA", "Team 4")
team2 = ("Majors", "Team 1")
for day in days_of_year:
    prob += (
        lpSum([slots_vars[i, team1[0], team1[1], k] for i in slots for k in teams_by_division[team1[0]]])  # team1 home
        + lpSum([slots_vars[i, team1[0], k, team1[1]] for i in slots for k in teams_by_division[team1[0]]])  # team1 away
        + lpSum([slots_vars[i, team2[0], team2[1], k] for i in slots for k in teams_by_division[team2[0]]])  # team2 home
        + lpSum([slots_vars[i, team2[0], k, team2[1]] for i in slots for k in teams_by_division[team2[0]]])  # team2 away
    ) >= 1, f"James_Baird_{team1[0]}_{team2[0]}_day_{day}"


logger.info("Solving")
# Solve (quietly)
# prob.solve(PULP_CBC_CMD(msg=0))
prob.solve()
if prob.status != 1:
    print("No solution found")
    print(prob.status)
    sys.exit(1)


check_count = Counter()
for v in prob.variables():
    if v.varValue > 0:
        # gross text parsing
        d = v.name.replace("Slot_", "").replace(",_", ",").replace("'", "").replace("(", "").replace(")", "")
        (id, division, home, away) = d.split(",")
        id = int(id)
        home = home.replace("_", " ")
        away = away.replace("_", " ")
        division = division.replace("_", " ")

        # Apply change
        print(f"Slot {id} \tDivision: {division} \tHome: {home} \tAway: {away}")
        assign_row(cFrame, id, division, home, away, safe=False)

        check_count[home] += 1
        check_count[away] += 1
        check_count["total"] += 1


# Balance hack
for i in range(100):
    balance_home_away(cFrame)


save_frame(cFrame, "calendar.pkl")


publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")


aFrame = analyze_columns(cFrame)
publish_df_to_gsheet(aFrame, worksheet_name="Analysis")
uFrame = cFrame.query("Division != Division")
publish_df_to_gsheet(uFrame, worksheet_name="Unassigned")
