import pandas as pd
import logging
from frametools import (
    analyze_columns,
    swap_rows_by_game_id,
    balance_home_away,
    swap_rows_by_slot,
    list_teams_for_division,
    assign_row,
    clear_division,
)
from gsheets import publish_df_to_gsheet
from helpers import short_division_names
from inputs import division_info
import re
from pulp import *
from collections import Counter


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

# Load division data
logger.info("Loading teams data")
save_file = "data/teams.pkl"
tFrame = pd.read_pickle(save_file)


############################################################################################################
### PULP STUFF

division = "Majors"
day_off = "Thursday"
games_per_team = 15

game_total = 10 * games_per_team / 2
teams = list_teams_for_division(division, tFrame)

# Data cleanup
cleanFrame = cFrame[cFrame["Week_Number"] != "UNKNOWN"].copy()

# Working Slots
correct_time = (cleanFrame["Time_Length"] == "150") & (pd.isna(cleanFrame["Week_Number"]) == False)

non_blocked = (
    (cleanFrame["Notes"] != "Opening Day Ceremony")
    & (cleanFrame["Day_of_Week"] != day_off)
    & (pd.to_numeric(cleanFrame["Week_Number"]) < 10)
)
minors_or_none = (cleanFrame["Division"] == division) | (pd.isna(cleanFrame["Division"]) == True)
slot_mask = correct_time & non_blocked & minors_or_none
working_slots = cleanFrame[slot_mask]

print(f"Usable Slots: {len(working_slots)}")

# Extract series we need from working_slots
days_of_week = working_slots["Day_of_Week"].unique()
days_of_year = working_slots["Day_of_Year"].unique()
weeks = working_slots["Week_Name"].unique()

############################################################################################################

# Slot Variables
slot_ids = working_slots.index

# Create every combination of slot, home team, away team as a LPvariable dict
slots_vars = pulp.LpVariable.dicts("Slot", [(s, h, a) for s in slot_ids for h in teams for a in teams], cat="Binary")

prob = LpProblem("League scheduling", LpMinimize)

# objective minimize games played
prob += lpSum([slots_vars]), "Number of games played should be minimized"  # Odd objective function?

# Total number of games
prob += lpSum([slots_vars[i] for i in slots_vars]) == game_total, "Total number of games played"

# Set games per team
for j in teams:
    prob += (
        lpSum([slots_vars[i, j, k] for i in slot_ids for k in teams])
        + lpSum([slots_vars[i, k, j] for i in slot_ids for k in teams])
    ) == games_per_team, f"Total_games_per_team_{j}"

# 1 game per slot
for i in slot_ids:
    prob += lpSum([slots_vars[i, j, k] for j in teams for k in teams]) <= 1, f"Only_one_game_per_slot_{i}"

# team cannot play itself
for i in slot_ids:
    prob += lpSum([slots_vars[i, j, k] for j in teams for k in teams if j == k]) == 0, f"sameteam_{i}"

# All teams must play each other at least once
for j in teams:
    for k in teams:
        if j != k:
            prob += (
                lpSum([slots_vars[i, j, k] for i in slot_ids]) + lpSum([slots_vars[i, k, j] for i in slot_ids])
            ) >= 1, f"Total_games_per_team_{j}_{k}"


# No team can play more than 1 game per day
for day in days_of_year:
    this_day = working_slots[working_slots["Day_of_Year"] == day].index
    for j in teams:
        prob += (
            (
                lpSum([slots_vars[i, j, k] for i in this_day for k in teams])
                + lpSum([slots_vars[i, k, j] for i in this_day for k in teams])  # home team on day  # away team on day
            )
            <= 1,
            f"Max_games_per_day_{day}_team_{j}",
        )

# No team can play back to back games
for day in days_of_year:
    this_day = working_slots[working_slots["Day_of_Year"] == day].index
    next_day = working_slots[working_slots["Day_of_Year"] == str(int(day) + 1)].index
    for j in teams:
        prob += (
            (
                lpSum([slots_vars[i, j, k] for i in this_day for k in teams])  # home team on day
                + lpSum([slots_vars[i, k, j] for i in this_day for k in teams])  # away team on day
                + lpSum([slots_vars[i, j, k] for i in next_day for k in teams])  # home team on day+1
                + lpSum([slots_vars[i, k, j] for i in next_day for k in teams])  # away team on day+1
            )
            <= 1,
            f"Max_backtoback_{day}_team_{j}",
        )

# 3 games in 5 days
for day in days_of_year:
    this_day = working_slots[working_slots["Day_of_Year"] == day].index
    next_day = working_slots[working_slots["Day_of_Year"] == str(int(day) + 1)].index
    third_day = working_slots[working_slots["Day_of_Year"] == str(int(day) + 2)].index
    fourth_day = working_slots[working_slots["Day_of_Year"] == str(int(day) + 3)].index
    fifth_day = working_slots[working_slots["Day_of_Year"] == str(int(day) + 4)].index
    for j in teams:
        prob += (
            (
                lpSum([slots_vars[i, j, k] for i in this_day for k in teams])  # home team on day
                + lpSum([slots_vars[i, k, j] for i in this_day for k in teams])  # away team on day
                + lpSum([slots_vars[i, j, k] for i in next_day for k in teams])  # home team on day+1
                + lpSum([slots_vars[i, k, j] for i in next_day for k in teams])  # away team on day+1
                + lpSum([slots_vars[i, j, k] for i in third_day for k in teams])  # home team on day+2
                + lpSum([slots_vars[i, k, j] for i in third_day for k in teams])  # away team on day+2
                + lpSum([slots_vars[i, j, k] for i in fourth_day for k in teams])  # home team on day+3
                + lpSum([slots_vars[i, k, j] for i in fourth_day for k in teams])  # away team on day+3
                + lpSum([slots_vars[i, j, k] for i in fifth_day for k in teams])  # home team on day+4
                + lpSum([slots_vars[i, k, j] for i in fifth_day for k in teams])  # home team on day+4
            )
            <= 3,
            f"Max_three_five_{day}_team_{j}",
        )


# Minimize games played against a single opponent
for k in teams:
    for j in teams:
        if i != j:
            prob += lpSum([slots_vars[i, j, k] + slots_vars[i, k, j] for i in slot_ids]) <= 2, f"Max_faceoffs_{k}_vs_{j}"


# No team can play more than 2 games per week
for week in weeks:
    slots_in_week = working_slots[working_slots["Week_Name"] == week].index
    for j in teams:
        prob += (
            (
                lpSum([slots_vars[i, j, k] for i in slots_in_week] for k in teams)
                + lpSum([slots_vars[i, k, j] for i in slots_in_week] for k in teams)
            )
            <= 2,
            f"Max_games_per_week_{week}_team_{j}",
        )


# Minimize weekday games
weekdays = ["Monday", "Tuesday", "Thursday", "Friday"]
weekday_slots = working_slots[working_slots["Day_of_Week"].isin(weekdays)].index
for j in teams:
    prob += (
        5
        * (
            lpSum([slots_vars[i, j, k] for i in weekday_slots for k in teams])  # home team on weekday
            + lpSum([slots_vars[i, k, j] for i in weekday_slots for k in teams])  # away team on weekday
        ),
        f"Max_weekdays_team_{j}",
    )


# Everyone plays Kimbell at least once
kimbell = ["Kimbell D1 NW", "Kimbell D2 SE"]
kimbell_slots = working_slots[working_slots["Field"].isin(kimbell)].index
for j in teams:
    prob += (
        (
            lpSum([slots_vars[i, j, k] for i in kimbell_slots] for k in teams)  # home team on kimbell
            + lpSum([slots_vars[i, k, j] for i in kimbell_slots] for k in teams) # away team on kimbell
        )
        >= 1,
        f"get_kimbell_team_{j}",
    )

ti_slots = working_slots[working_slots["location"] == "TI"].index
for j in teams:
    prob += (
        (
            lpSum([slots_vars[i, j, k] for i in ti_slots] for k in teams)  # home team on ti
            + lpSum([slots_vars[i, k, j] for i in ti_slots] for k in teams) # away team on ti
        )
        >= 6,
        f"get_ti_team_{j}",
    )



tuesday_slots = working_slots[working_slots["Day_of_Week"] == "Tuesday"].index
for j in teams:
    prob += (
        (
            lpSum([slots_vars[i, j, k] for i in tuesday_slots] for k in teams)  # home team on tuesday
            + lpSum([slots_vars[i, k, j] for i in tuesday_slots] for k in teams) # away team on tuesday
        )
        >= 2,
        f"get_tuesday_team_{j}",
    )


# Majors off "Ft. Scott - South"" and "Rossi Park #1"
skip_fields = ["Ft. Scott - South", "Rossi Park #1", "Kimbell D3 SW"]
fss_slots = working_slots[working_slots["Field"].isin(skip_fields)].index
#fss_slots = working_slots[working_slots["Field"] == "Ft. Scott - South"].index
for j in teams:
    prob += (
        (
            lpSum([slots_vars[i, j, k] for i in fss_slots] for k in teams)  # home team on fss
            + lpSum([slots_vars[i, k, j] for i in fss_slots] for k in teams) # away team on fss
        )
        == 0,
        f"fss_team_{j}",
    )


# even weekends
weekends = ["Saturday", "Sunday"]
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(weekends)].index
for j in teams:
    prob += (
        (
            lpSum([slots_vars[i, j, k] for i in weekend_slots] for k in teams)  # home team on tepper weekend
            + lpSum([slots_vars[i, k, j] for i in weekend_slots] for k in teams) # away team on tepper weekend
        )
        >= 6,
        f"get_weekend_team_{j}",
    )


# Prefer tepper on weekends
tepper = ["Tepper"]
tepper_slots = working_slots[working_slots["Field"].isin(tepper)].index
weekends = ["Saturday", "Sunday"]
weekend_slots = working_slots[working_slots["Day_of_Week"].isin(weekends)].index
tepper_weekend_slots = list(set(tepper_slots).intersection(weekend_slots))
for j in teams:
    prob += (
        (
            lpSum([slots_vars[i, j, k] for i in tepper_weekend_slots] for k in teams)  # home team on tepper weekend
            + lpSum([slots_vars[i, k, j] for i in tepper_weekend_slots] for k in teams) # away team on tepper weekend
        )
        >= 2,
        f"get_tepper_weekend_team_{j}",
    )

ketcham = ["Ketcham"]
ketcham_slots = working_slots[working_slots["Field"].isin(tepper)].index
for j in teams:
    prob += (
        (
            lpSum([slots_vars[i, j, k] for i in ketcham_slots] for k in teams)  # home team on tepper weekend
            + lpSum([slots_vars[i, k, j] for i in ketcham_slots] for k in teams) # away team on tepper weekend
        )
        <= 7,
        f"get_kechamd_team_{j}",
    )


tuesday_slots = working_slots[working_slots["Day_of_Week"] == "Wednesday"].index
for j in teams:
    prob += (
        (
            lpSum([slots_vars[i, j, k] for i in tuesday_slots] for k in teams)  # home team on tuesday
            + lpSum([slots_vars[i, k, j] for i in tuesday_slots] for k in teams) # away team on tuesday
        )
        <= 5,
        f"weds{j}",
    )


# Solve (quietly)
prob.solve(PULP_CBC_CMD(msg=0))

clear_division(cFrame, division)

check_count = Counter()
for v in prob.variables():
    if v.varValue > 0:
        # gross text parsing
        d = v.name.replace("Slot_", "").replace(",_", ",").replace("'", "").replace("(", "").replace(")", "")
        (id, home, away) = d.split(",")
        id = int(id)
        home = home.replace("_", " ")
        away = away.replace("_", " ")

        # Apply change
        #print(f"Slot {id} Home: {home} Away: {away}")
        #assign_row(cFrame, id, division, home, away, safe=False)

        check_count[home] += 1
        check_count[away] += 1
        check_count["total"] += 1


for foo in check_count:
    print(f"{foo}: {check_count[foo]}")

if check_count["total"] > game_total:
    print("Too many games???")
    sys.exit(1)


for v in prob.variables():
    if v.varValue > 0:
        # gross text parsing
        d = v.name.replace("Slot_", "").replace(",_", ",").replace("'", "").replace("(", "").replace(")", "")
        (id, home, away) = d.split(",")
        id = int(id)
        home = home.replace("_", " ")
        away = away.replace("_", " ")

        # Apply change
        print(f"Slot {id} Home: {home} Away: {away}")
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
