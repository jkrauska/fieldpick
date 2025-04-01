import pandas as pd
import logging
import warnings
from frametools import (
    analyze_columns,
    balance_home_away,
    assign_row,
    clear_division,
    save_frame,
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


weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekends = ["Saturday", "Sunday"]

##########################################################################
# PULP STUFF


# Data cleanup
cleanFrame = cFrame[cFrame["Week_Number"] != "UNKNOWN"].copy()

# Working Slots
correct_time = (cleanFrame["Time_Length"] == "180") & (
    pd.isna(cleanFrame["Week_Number"]) == False)
not_riordan = (cleanFrame["Field"] != "Riordan")
non_blocked = (cleanFrame["Notes"] != "Opening Day Ceremony")
less_than_10 = (pd.to_numeric(cleanFrame["Week_Number"]) < 10)

slot_mask = correct_time & non_blocked & less_than_10 & not_riordan

working_slots = cleanFrame[slot_mask]

print(f"Usable Slots: {len(working_slots)}")

print(working_slots)


# Extract series we need from working_slots
days_of_week = working_slots["Day_of_Week"].unique()
days_of_year = working_slots["Day_of_Year"].unique()
weeks = working_slots["Week_Name"].unique()
fields = working_slots["Field"].unique()

# Extract Divisions
divisions = list(tFrame["Division"].unique())
# Remove non-150 divisions
for non150 in [
    "Tee Ball",
    "Upper Farm",
    "Lower Farm",
    "Challenger",
    "Rookie",
    "Minors AA",
    "Minors AAA",
        "Majors"]:
    try:
        divisions.remove(non150)
    except BaseException:
        pass

# Remove all division data
for division in divisions:
    clear_division(cFrame, division)


print(f"Divisions: {divisions}")


##########################################################################

# Slot Variables
slots = working_slots.index

# Helpful Dict of each division's teams
teams_by_division = {}
for division in divisions:
    teams_by_division[division] = tFrame[tFrame["Division"]
                                         == division]["Team"].unique()


print(f"Teams by Division: {teams_by_division}")


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

# prob = LpProblem("League scheduling", LpMinimize)
prob = LpProblem("League scheduling", LpMaximize)


# objective minimize games played
# Odd objective function?
prob += lpSum([slots_vars]), "Number of games played should be minimized"


# Set games per team

for division in divisions:
    games_per_team = division_info[division]["games"]
    print(f"Games per team: {games_per_team}")
    teams = teams_by_division[division]
    for j in teams:
        prob += (
            lpSum([slots_vars[i, division, j, k] for i in slots for k in teams])
            + lpSum([slots_vars[i, division, k, j] for i in slots for k in teams])
        ) == 10, f"Games_per_team_{division}_{j}"


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

# Team cannot play itself
for division in divisions:
    teams = teams_by_division[division]
    for i in slots:
        prob += (lpSum([slots_vars[i,
                                   division,
                                   j,
                                   k] for j in teams for k in teams if j == k]) == 0,
                 f"No_Same_Team_{division}_{i}",
                 )


# All teams must play each other at least once
for division in divisions:
    teams = teams_by_division[division]
    for j in teams:
        for k in teams:
            if j != k:
                prob += (lpSum([slots_vars[i, division, j, k] for i in slots]) + lpSum(
                    [slots_vars[i, division, k, j] for i in slots])) >= 1, f"Min_games_per_pair_{division}_{j}_{k}"

# # No team should play the same team more than twice
for division in divisions:
    teams = teams_by_division[division]
    for j in teams:
        for k in teams:
            if j != k:
                prob += (lpSum([slots_vars[i, division, j, k] for i in slots]) + lpSum(
                    [slots_vars[i, division, k, j] for i in slots])) <= 2, f"Max_games_per_pair_{division}_{j}_{k}"


# # No team should play more than 2 games per week
for week in weeks:
    this_week = working_slots[working_slots["Week_Name"] == week].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                (
                    lpSum([slots_vars[i, division, j, k]
                          for i in this_week for k in teams])
                    + lpSum(
                        [slots_vars[i, division, k, j]
                            for i in this_week for k in teams]
                    )  # home team on week  # away team on week
                )
                <= 2,
                f"Max_two_games_per_week_{division}_{week}_team_{j}",
            )

# Min one week except for W1 and W6

# for week in weeks:
#     if week in ["Week 1", "Week 6"]:
#         continue
#     this_week = working_slots[working_slots["Week_Name"] == week].index
#     for division in divisions:
#         teams = teams_by_division[division]
#         for j in teams:
#             prob += (
#                 (
#                     lpSum([slots_vars[i, division, j, k] for i in this_week for k in teams])
#                     + lpSum(
#                         [slots_vars[i, division, k, j] for i in this_week for k in teams]
#                     )  # home team on week  # away team on week
#                 )
#                 >= 1,
#                 f"Min_one_games_per_week_{division}_{week}_team_{j}",
#             )

# Block denied fields
# for division in divisions:
#     denied_fields = division_info[division].get("denied_fields", [])
#     logger.info(f"{division} denied_fields: {denied_fields}")
#     denied_fields_slots = working_slots[working_slots["Field"].isin(denied_fields)].index
#     teams = teams_by_division[division]
#     prob += (
#         lpSum([slots_vars[i, division, j, k] for i in denied_fields_slots  for j in teams for k in teams])
#     ) == 0, f"Denied_fields_{division}"


# No team can play more than 1 game per day
for day in days_of_year:
    this_day = working_slots[working_slots["Day_of_Year"] == day].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                (
                    lpSum([slots_vars[i, division, j, k]
                          for i in this_day for k in teams])
                    + lpSum(
                        [slots_vars[i, division, k, j]
                            for i in this_day for k in teams]
                    )  # home team on day  # away team on day
                )
                <= 1,
                f"Max_games_per_day_{division}_{day}_team_{j}",
            )


# No team can play back to back games
for day in days_of_year:
    this_day = working_slots[working_slots["Day_of_Year"] == day].index
    next_day = working_slots[working_slots["Day_of_Year"]
                             == str(int(day) + 1)].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                (
                    lpSum([slots_vars[i, division, j, k]
                          # home team on day
                           for i in this_day for k in teams])
                    + lpSum([slots_vars[i, division, k, j]
                            # away team on day
                             for i in this_day for k in teams])
                    + lpSum([slots_vars[i, division, j, k]
                            # home team on day+1
                             for i in next_day for k in teams])
                    + lpSum([slots_vars[i, division, k, j]
                            # away team on day+1
                             for i in next_day for k in teams])
                )
                <= 2,
                f"Back_to_back_{division}_{day}_team_{j}",
            )

# for day in days_of_year:
#     this_day = working_slots[working_slots["Day_of_Year"] == day].index
#     next_day = working_slots[working_slots["Day_of_Year"] == str(int(day) + 1)].index
#     for division in divisions:
#         teams = teams_by_division[division]
#         for j in teams:

#             by_day =  (
#                 (
#                     lpSum([slots_vars[i, division, j, k] for i in this_day for k in teams])  # home team on day
#                     + lpSum([slots_vars[i, division, k, j] for i in this_day for k in teams])  # away team on day
#                     + lpSum([slots_vars[i, division, j, k] for i in next_day for k in teams])  # home team on day+1
#                     + lpSum([slots_vars[i, division, k, j] for i in next_day for k in teams])  # away team on day+1
#                 )
#                 <= 2,
#                 f"Back_to_back_{division}_{day}_team_{j}",
#             )

#             prob += by_day


division = "Juniors"

lockteam = "Team 1"
lockweek = "Week 2"

weekend_slots = working_slots[working_slots["Day_of_Week"].isin(
    weekends)].index

for week in weeks:
    if week == lockweek:  # hot week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) == 2, f"Assign {lockteam} back to back in week {week}"
    else:  # cold week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) <= 1, f"Block {lockteam} back to back in week {week}"


lockteam = "Team 2"
lockweek = "Week 3"
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(
    weekends)].index
for week in weeks:
    if week == lockweek:  # hot week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) == 2, f"Assign {lockteam} back to back in week {week}"
    else:  # cold week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) <= 1, f"Block {lockteam} back to back in week {week}"

lockteam = "Team 3"
lockweek = "Week 4"
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(
    weekends)].index
for week in weeks:
    if week == lockweek:  # hot week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) == 2, f"Assign {lockteam} back to back in week {week}"
    else:  # cold week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) <= 1, f"Block {lockteam} back to back in week {week}"

lockteam = "Team 4"
lockweek = "Week 5"
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(
    weekends)].index
for week in weeks:
    if week == lockweek:  # hot week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) == 2, f"Assign {lockteam} back to back in week {week}"
    else:  # cold week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) <= 1, f"Block {lockteam} back to back in week {week}"

lockteam = "Team 5"
lockweek = "Week 7"
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(
    weekends)].index
for week in weeks:
    if week == lockweek:  # hot week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) == 2, f"Assign {lockteam} back to back in week {week}"
    else:  # cold week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) <= 1, f"Block {lockteam} back to back in week {week}"

lockteam = "Team 6"
lockweek = "Week 8"
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(
    weekends)].index
for week in weeks:
    if week == lockweek:  # hot week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) == 2, f"Assign {lockteam} back to back in week {week}"
    else:  # cold week
        this_week = working_slots[working_slots["Week_Name"] == week].index
        weekend_slots_this_week = weekend_slots.intersection(this_week)
        prob += (
            lpSum([slots_vars[slot, division, lockteam, k]
                  for slot in weekend_slots_this_week for k in teams])  # home team on day
            + lpSum([slots_vars[slot, division, k, lockteam]
                    for slot in weekend_slots_this_week for k in teams])  # away team on day
        ) <= 1, f"Block {lockteam} back to back in week {week}"


# # No team can play 3 games in 5 days
for day in days_of_year:
    day_one = working_slots[working_slots["Day_of_Year"] == day].index
    day_two = working_slots[working_slots["Day_of_Year"]
                            == str(int(day) + 1)].index
    day_three = working_slots[working_slots["Day_of_Year"] == str(
        int(day) + 2)].index
    day_four = working_slots[working_slots["Day_of_Year"]
                             == str(int(day) + 3)].index
    day_five = working_slots[working_slots["Day_of_Year"]
                             == str(int(day) + 4)].index

    five_days = list(day_one) + list(day_two) + \
        list(day_three) + list(day_four) + list(day_five)

    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                (
                    lpSum([slots_vars[i, division, j, k]
                          # home team on day
                           for i in five_days for k in teams])
                    + lpSum([slots_vars[i, division, k, j]
                            # away team on day
                             for i in five_days for k in teams])
                )
                <= 2,
                f"3_games_in_5_days_{division}_{day}_team_{j}",
            )

# # No team can should play 3 games in 6 days more than once
# for day in days_of_year:
#     day_one = working_slots[working_slots["Day_of_Year"] == day].index
#     day_two = working_slots[working_slots["Day_of_Year"] == str(int(day) + 1)].index
#     day_three = working_slots[working_slots["Day_of_Year"] == str(int(day) + 2)].index
#     day_four = working_slots[working_slots["Day_of_Year"] == str(int(day) + 3)].index
#     day_five = working_slots[working_slots["Day_of_Year"] == str(int(day) + 4)].index
#     day_six = working_slots[working_slots["Day_of_Year"] == str(int(day) + 5)].index

#     six_days = list(day_one) + list(day_two) + list(day_three) + list(day_four) + list(day_five) + list(day_six)
#     for division in divisions:
#         teams = teams_by_division[division]
#         for j in teams:
#             prob += (
#                 (
#                     lpSum([slots_vars[i, division, j, k] for i in six_days for k in teams])  # home team on day
#                     + lpSum([slots_vars[i, division, k, j] for i in six_days for k in teams])  # away team on day
#                 )
#                 <= 2,  # Not sure about this...2 or 3?
#                 f"3_games_in_6_days_{division}_{day}_team_{j}",
#             )


# # # More than 1 Paul Goode Main
fields = ["Paul Goode Main"]
for field in fields:
    field_slots = working_slots[working_slots["Field"] == field].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                lpSum([slots_vars[i, division, j, k] for i in field_slots for k in teams])
                + lpSum([slots_vars[i, division, k, j] for i in field_slots for k in teams])
            ) >= 1, f"More_than_1_{field}_{division}_{j}"

# # # more than 1 McCoppin
fields = ["McCoppin"]
for field in fields:
    field_slots = working_slots[working_slots["Field"] == field].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                lpSum([slots_vars[i, division, j, k] for i in field_slots for k in teams])
                + lpSum([slots_vars[i, division, k, j] for i in field_slots for k in teams])
            ) >= 1, f"More_than_1_{field}_{division}_{j}"


fields = ["Balboa - Sweeney"]
for field in fields:
    field_slots = working_slots[working_slots["Field"] == field].index
    for division in divisions:
        teams = teams_by_division[division]
        for j in teams:
            prob += (
                lpSum([slots_vars[i, division, j, k] for i in field_slots for k in teams])
                + lpSum([slots_vars[i, division, k, j] for i in field_slots for k in teams])
            ) >= 1, f"More_than_1_{field}_{division}_{j}"

# # No single field used more than games_per_team / 2
# for field in fields:
#     field_slots = working_slots[working_slots["Field"] == field].index
#     for division in divisions:
#         teams = teams_by_division[division]
#         for j in teams:
#             prob += (
#                 lpSum([slots_vars[i, division, j, k] for i in field_slots for k in teams])
#                 + lpSum([slots_vars[i, division, k, j] for i in field_slots for k in teams])
#             ) <= int(games_per_team / 2) - 1, f"Single_field_{field}_{division}_{j}"


# # Try to balance Weekday and Weekend
# weekday_slots = working_slots[working_slots["Day_of_Week"].isin(weekdays)].index
# weekend_slots = working_slots[working_slots["Day_of_Week"].isin(weekends)].index
# for division in divisions:
#     teams = teams_by_division[division]
#     for j in teams:
#         # wd - we <= 2

#         prob += (
#             lpSum([slots_vars[i, division, j, k] for i in weekday_slots for k in teams])
#             + lpSum([slots_vars[i, division, k, j] for i in weekday_slots for k in teams])
#             - lpSum([slots_vars[i, division, j, k] for i in weekend_slots for k in teams])
#             - lpSum([slots_vars[i, division, k, j] for i in weekend_slots for k in teams])
#         ) <= 1, f"Weekday_Weekend_{division}_{j}"

#         # we - wd <= 2

#         prob += (
#             lpSum([slots_vars[i, division, j, k] for i in weekend_slots for k in teams])
#             + lpSum([slots_vars[i, division, k, j] for i in weekend_slots for k in teams])
#             - lpSum([slots_vars[i, division, j, k] for i in weekday_slots for k in teams])
#             - lpSum([slots_vars[i, division, k, j] for i in weekday_slots for k in teams])
#         ) <= 1, f"Weekend_Weekday_{division}_{j}"


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
        d = v.name.replace(
            "Slot_",
            "").replace(
            ",_",
            ",").replace(
            "'",
            "").replace(
                "(",
                "").replace(
                    ")",
            "")
        (id, division, home, away) = d.split(",")
        id = int(id)
        home = home.replace("_", " ")
        away = away.replace("_", " ")
        division = division.replace("_", " ")

        # Apply change
        print(
            f"Slot {id} \tDivision: {division} \tHome: {home} \tAway: {away}")
        assign_row(cFrame, id, division, home, away, safe=False)

        check_count[home] += 1
        check_count[away] += 1
        check_count["total"] += 1


# sys.exit(1)

# Balance hack
for i in range(100):
    balance_home_away(cFrame)


save_frame(cFrame, "calendar.pkl")

publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")


aFrame = analyze_columns(cFrame)
publish_df_to_gsheet(aFrame, worksheet_name="Analysis")
uFrame = cFrame.query("Division != Division")
publish_df_to_gsheet(uFrame, worksheet_name="Unassigned")
