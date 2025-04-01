import pandas as pd
import math
import logging
from frametools import (load_frame, save_frame,
                        balance_home_away,
                        list_teams_for_division,
                        assign_row,
                        clear_division,
                        )
from inputs import (division_info)
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, PULP_CBC_CMD, LpStatus
from pulpFunctions import minimum_games_per_team
from collections import Counter
import sys

from pulpFunctions import (
    one_game_per_slot,
    cannot_play_yourself,
    limit_faceoffs,
    no_back_to_back,
    limit_3_in_5,
    limit_games_per_day,
    limit_games_per_week,
    early_starts,
    field_limits,
    minimum_games_per_team,
    minimum_faceoffs,
    set_field_ratios, solveMe
)

logging.basicConfig(
    format="%(asctime)s %(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger()


# Load data
cFrame = load_frame("data/calendar.pkl")
tFrame = load_frame("data/teams.pkl")

pd.set_option('display.max_rows', None)


##########################################################################
# PULP STUFF

division = "Upper Farm"
teams = list_teams_for_division(division, tFrame)

duration = "120"
day_off = "Monday"
last_week = "12"

games_per_team = 10
# game_total = 14 * games_per_team / 2

# Data cleanup
cleanFrame = cFrame[cFrame["Week_Number"] != "UNKNOWN"].copy()

# Build filters based on slot criteria
duration_correct = cleanFrame["Time_Length"] == duration
valid_week_number = (pd.isna(cleanFrame["Week_Number"]) == False)
correct_time = duration_correct & valid_week_number

division_same = cleanFrame["Division"] == division
division_not_set = (pd.isna(cleanFrame["Division"]))
slot_good_for_division = division_same | division_not_set

before_last_week = (pd.to_numeric(cleanFrame["Week_Number"]) <= int(last_week))
not_day_off = cleanFrame["Day_of_Week"] != day_off
not_opening_day = cleanFrame["Notes"] != "Opening Day Ceremony"
non_blocked = (not_opening_day & not_day_off & before_last_week)

# Prescribed slots
prescribed_fields = cleanFrame["Intended_Division"] == division
print(f"Prescribed Slots: {prescribed_fields.sum()}")
prescribed = prescribed_fields

# Combined filters
slot_mask = correct_time & non_blocked & slot_good_for_division & prescribed
working_slots = cleanFrame[slot_mask]

print(f"Working slots: {len(working_slots)}")

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

field_ratios = set_field_ratios(working_slots)


##########################################################################

# Slot Variables
slot_ids = working_slots.index
print(f"Usable Slots: {len(working_slots)}")

# Create every combination of slot, home team, away team as a LPvariable dict
combinations = [(s, h, a) for s in slot_ids for h in teams for a in teams]
slots_vars = LpVariable.dicts("Slot", combinations, cat="Binary")

_division = division.replace(" ", "_")
prob = LpProblem(f"League_Scheduling_{_division}", LpMaximize)

# objective maximize number of slots used
prob += lpSum([slots_vars]), "Number of games played"

# Basic constraints
prob = one_game_per_slot(prob, slots_vars, teams, slot_ids)
prob = cannot_play_yourself(prob, slots_vars, teams, slot_ids)

# Same vs Same
prob = minimum_faceoffs(prob, slots_vars, teams, slot_ids, limit=0)
prob = limit_faceoffs(prob, slots_vars, teams, slot_ids, limit=1)

# Limit consecutive games
prob = no_back_to_back(prob, days_of_year, working_slots, slots_vars, teams)
prob = limit_3_in_5(prob, days_of_year, working_slots, slots_vars, teams)

# Limit games per day and per week
prob = limit_games_per_day(
    prob,
    days_of_year,
    working_slots,
    slots_vars,
    teams,
    limit=1)
prob = limit_games_per_week(
    prob,
    weeks,
    working_slots,
    slots_vars,
    teams,
    limit=1)


prob = minimum_games_per_team(
    prob,
    teams,
    slots_vars,
    slot_ids,
    min_games=games_per_team)

prob = early_starts(prob, teams, slots_vars, early_slots, min=3, max=5)

# Balance fields
for field in field_ratios:
    min = math.floor(field_ratios[field] * games_per_team) - 1
    max = math.ceil(field_ratios[field] * games_per_team) + 1
    prob = field_limits(
        prob,
        teams,
        working_slots,
        slots_vars,
        field,
        min,
        max)


# Solve (quietly)
prob = solveMe(prob, working_slots)
clear_division(cFrame, division)

check_count = Counter()
for v in prob.variables():
    if v.varValue:
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
            # Apply change
            # print(f"Slot {id} Home: {home} Away: {away}")
            assign_row(cFrame, id, division, home, away, safe=False)

            check_count[home] += 1
            check_count[away] += 1
            check_count["Total Games"] += 1


for foo in sorted(check_count.keys(), ):
    print(f"Checking: {foo}: {check_count[foo]}")


# Balance hack
for i in range(100):
    balance_home_away(cFrame)


save_frame(cFrame, "calendar.pkl")
