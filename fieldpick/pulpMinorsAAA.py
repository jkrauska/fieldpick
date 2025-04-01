import pandas as pd
import logging
from frametools import (
    balance_home_away,
    list_teams_for_division,
    assign_row,
    clear_division,
)

from pulp import LpProblem, LpVariable, LpMaximize, lpSum
from collections import Counter
import sys

from frametools import (
    load_frame,
    save_frame,
)

from pulpFunctions import (
    common_constraints,
    limit_faceoffs,
    minimum_faceoffs,
    limit_games_per_week,
    early_starts,
    field_limits,
    balance_fields,
    minimum_games_per_team,
    maximum_games_per_team,
    min_home_games,
    min_weekends,
    min_ti,
    max_ti,
    max_ti_weekdays,
    no_6_in_21,
    min_games_per_week,
    solveMe,
)

logging.basicConfig(
    format="%(asctime)s %(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger()


# Load data
cFrame: pd.DataFrame = load_frame("data/calendar.pkl")
tFrame = load_frame("data/teams.pkl")

pd.set_option("display.max_rows", None)


##########################################################################
# PULP STUFF

division = "Minors AAA"
teams = list_teams_for_division(division, tFrame)

duration = "150"
last_week = "9"

games_per_team = 12

# Data cleanup
cleanFrame = cFrame[cFrame["Week_Number"] != "UNKNOWN"].copy()

# Build filters based on slot criteria
duration_correct = cleanFrame["Time_Length"] == duration
valid_week_number = pd.isna(cleanFrame["Week_Number"]) == False
correct_time = duration_correct & valid_week_number

division_same = cleanFrame["Division"] == division
division_not_set = pd.isna(cleanFrame["Division"])
slot_good_for_division = division_same | division_not_set

before_last_week = pd.to_numeric(cleanFrame["Week_Number"]) <= int(last_week)
not_opening_day = cleanFrame["Notes"] != "Opening Day Ceremony"
non_blocked = not_opening_day & before_last_week


# Prescribed slots
divisions = [division, "Majors"]
prescribed_fields = cleanFrame["Intended_Division"].isin(divisions)
print(f"Prescribed Slots2: {prescribed_fields.sum()}")
prescribed = prescribed_fields


# Combined filters
slot_mask = correct_time & non_blocked & slot_good_for_division & prescribed
working_slots = cleanFrame[slot_mask]

if len(working_slots) < 1:
    print(f"No slots found for {division}")
    print(cleanFrame)
    sys.exit(1)

# Extract series we need from working_slots
days_of_week = working_slots["Day_of_Week"].unique()
days_of_year = working_slots["Day_of_Year"].unique()
weeks = working_slots["Week_Name"].unique()

early_times = ["08:00", "08:30", "09:00", "09:30"]
early_slots = working_slots[working_slots["Start"].isin(early_times)].index


##########################################################################

# Slot Variables
slot_ids = working_slots.index
print(f"Usable Slots: {len(working_slots)}")

# Create every combination of slot, home team, away team as a LPvariable dict
combinations = [(s, h, a) for s in slot_ids for h in teams for a in teams]
slots_vars = LpVariable.dicts("Slot", combinations, cat="Binary")

_division = division.replace(" ", "_")
prob = LpProblem(f"League_Scheduling_{_division}", LpMaximize)

# objective maximize number of slots used at desired fields, and prefer
# weekends

desired_field = [
    "Tepper - Field 1",
    "West Sunset - Field 3",
    "South Sunset - Diamond 1"]
desired_slots = working_slots[working_slots["Full_Field"].isin(
    desired_field)].index

# Prefer weekend slots
weekends = ["Saturday", "Sunday"]
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(
    weekends)].index
prob += lpSum([10 * slots_vars[i, h, a] for i in desired_slots for h in teams for a in teams]) + \
    lpSum([slots_vars[i, h, a] for i in weekend_slots for h in teams for a in teams]), "Combined objective: desired fields and weekend slots"

# Common constraints
prob = common_constraints(prob, slots_vars, teams, slot_ids, working_slots)

# Division Specific
prob = minimum_faceoffs(prob, slots_vars, teams, slot_ids, limit=1)
prob = limit_faceoffs(prob, slots_vars, teams, slot_ids, limit=2)
prob = limit_games_per_week(
    prob,
    weeks,
    working_slots,
    slots_vars,
    teams,
    limit=2)

prob = minimum_games_per_team(
    prob,
    teams,
    slots_vars,
    slot_ids,
    min_games=games_per_team)
prob = maximum_games_per_team(
    prob,
    teams,
    slots_vars,
    slot_ids,
    max_games=games_per_team)
prob = early_starts(prob, teams, slots_vars, early_slots, min=3, max=4)

# Ensure each team has at least half of their games as home games
prob = min_home_games(prob, teams, working_slots, slots_vars, min_games=games_per_team // 2)

# # Balance fields
prob = balance_fields(
    prob,
    teams,
    games_per_team,
    working_slots,
    slots_vars,
    fudge=1)

# # Tepper Min
prob = field_limits(
    prob,
    teams,
    working_slots,
    slots_vars,
    "Tepper - Field 1",
    min=3,
    max=4,
    variation="TEPPER_MIN")

# Ensure at least one game at West Sunset - Field 3
prob = field_limits(
    prob,
    teams,
    working_slots,
    slots_vars,
    "West Sunset - Field 3",
    min=1,
    max=3,
    variation="WEST_SUNSET_MIN")

prob = min_weekends(prob, teams, working_slots, slots_vars, min=7)

prob = min_ti(prob, teams, working_slots, slots_vars, min=9)
prob = max_ti(prob, teams, working_slots, slots_vars, max=10)
prob = max_ti_weekdays(prob, teams, working_slots, slots_vars, max=4)
prob = no_6_in_21(prob, teams, working_slots, slots_vars)
prob = min_games_per_week(prob, teams, working_slots, slots_vars, min=1)

prob = solveMe(prob, working_slots)
clear_division(cFrame, division)

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
        (id, home, away) = d.split(",")
        id = int(id)

        check_count[home] += 1
        check_count[away] += 1
        check_count["total"] += 1


for foo in check_count:
    print(f"{foo}: {check_count[foo]}")


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
        (id, home, away) = d.split(",")
        id = int(id)
        assign_row(cFrame, id, division, home, away, safe=False)


# Balance hack
for i in range(100):
    balance_home_away(cFrame)


save_frame(cFrame, "calendar.pkl")
