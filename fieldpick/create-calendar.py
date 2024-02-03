from helpers import add_time_slots, fort_scott, tepper_ketcham, tuesday_thursday
import pandas as pd
import logging
from frametools import save_frame

logging.basicConfig(
    format="%(asctime)s %(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger()


# Override pandas display settings
pd.set_option("display.max_rows", 500)

# initialize calendar
cFrame = pd.DataFrame()


##################################################
# Tee Ball

# cFrame = add_time_slots(
#     locations=["Paul Goode"],
#     fields=["Practice"],
#     intended_division="Tee Ball",
#     days_of_week="Saturday",
#     start_day="3/2/2024",
#     end_day="5/19/2024",
#     times=[("09:00", "10:30"), ("10:30", "12:00")],
#     input=cFrame,
# )

cFrame = add_time_slots(
    locations=["Rossi"],
    fields=["Field 1"],
    intended_division="Tee Ball",
    days_of_week="Saturday",
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[("09:00", "10:30"), ("10:30", "12:00")],
    input=cFrame,
)


# tee 1.5h on Saturdays
cFrame = add_time_slots(
    locations=["Larsen"],
    fields=["Field 1"],
    intended_division="Tee Ball",
    days_of_week=["Saturday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("09:00", "10:30"),
        ("10:30", "12:00"),
        ("12:00", "13:30"),
        ("13:30", "15:00"),
    ],
    input=cFrame,
)

##################################################
# Lower Farm
cFrame = add_time_slots(
    locations=["Fort Scott"],
    fields=["South Diamond"],
    intended_division="Lower Farm",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("08:00", "10:00"),
        ("10:00", "12:00"),
        ("12:00", "14:00"),
    ],  # 2 h slots
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Larsen"],
    fields=["Field 1"],
    intended_division="Lower Farm",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("09:00", "11:00"),
        ("11:00", "13:00"),
        ("13:00", "15:00"),
    ],
    input=cFrame,
)

##################################################
# Upper Farm

cFrame = add_time_slots(
    locations=["Fort Scott"],
    fields=["North Diamond"],
    intended_division="Upper Farm",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("08:00", "10:00"),
        ("10:00", "12:00"),
        ("12:00", "14:00"),
    ],  # 2 h slots
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Laurel Hill"],
    fields=["Field 1"],
    intended_division="Upper Farm",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("09:00", "11:00"),
        ("11:00", "13:00"),
        ("13:00", "15:00"),
    ],
    input=cFrame,
)

##################################################
# Rookie
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Rookie",
    days_of_week=["Saturday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[("14:00", "16:30")],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Rossi"],
    fields=["Field 1"],
    intended_division="Rookie",
    days_of_week=["Saturday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("12:00", "14:30"),
        ("14:30", "17:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Rookie",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("11:00", "13:30"),
        ("13:30", "16:00"),
    ],
    input=cFrame,
)

# Weds
cFrame = add_time_slots(
    locations=["Kimbell"],
    fields=["Diamond 2"],
    intended_division="Rookie",
    days_of_week=["Wednesday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

# WORK IN PROGRESS
cFrame = add_time_slots(
    locations=["Kimbell"],
    fields=["Diamond 3"],
    intended_division="Rookie",
    days_of_week=["Wednesday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

# Thurs
cFrame = add_time_slots(
    locations=["South Sunset"],
    fields=["Diamond 2"],
    intended_division="Minors AA",
    days_of_week=["Thursday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

# Friday
cFrame = add_time_slots(
    locations=["South Sunset"],
    fields=["Diamond 2"],
    intended_division="Rookie",
    days_of_week=["Friday"],
    start_day="3/2/2024",
    end_day="5/19/2024",

    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)



##################################################
# AA Minors

# Sat
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Minors AA",
    days_of_week=["Saturday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[("16:30", "19:00")],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Minors AA",
    days_of_week=["Saturday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[("16:30", "19:00")],
    input=cFrame,
)

# Sunday
cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Minors AA",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[("08:30", "11:00")],
    input=cFrame,
)


cFrame = add_time_slots(
    locations=["Rossi"],
    fields=["Field 1"],
    intended_division="Minors AA",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("09:00", "11:30"),
        ("11:30", "14:00"),
    ],
    input=cFrame,
)

# Weds and Thurs inherited from Rookie

# Friday
cFrame = add_time_slots(
    locations=["South Sunset"],
    fields=["Diamond 1"],
    intended_division="Minors AA",
    days_of_week=["Friday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

##################################################
# AAA Minors

# Saturday
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Saturday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[("11:30", "14:00")],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Saturday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("11:30", "14:00"),
        ("14:00", "16:30"),
    ],
    input=cFrame,
)

# Sunday
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[("09:00", "11:30")],
    input=cFrame,
)


cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("16:00", "18:30"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham", "Tepper"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Tuesday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)


cFrame = add_time_slots(
    locations=["South Sunset"],
    fields=["Diamond 2"],
    intended_division="Minors AAA",
    days_of_week=["Tuesday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)


##################################################
# Majors

# Sat
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Saturday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[("09:00", "11:30")],
    input=cFrame,
)
cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Saturday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[("09:00", "11:30")],
    input=cFrame,
)

# Sunday
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("11:30", "14:00"),
        ("16:00", "18:30"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["West Sunset"],
    fields=["Field 3"],
    intended_division="Majors",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("09:00", "11:30"),
    ],
    input=cFrame,
)

# Overrides
# Change intended first week midweek to only allow Majors
ws3 = cFrame["Full_Field"] == "West Sunset - Field 3"
target_dates = ["2024-03-24", "2024-04-28"]
targets = cFrame["Date"].isin(target_dates)

cFrame.loc[
    (ws3) & (targets),
    "Intended_Division",
] = "Minors AA"


# Weds
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Wednesday", "Thursday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)
cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Wednesday", "Thursday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

# Give two Wednesdays to AA to get 12.
cFrame = add_time_slots(
    locations=["Kimbell"],
    fields=["Diamond 1"],
    intended_division="Minors AA",
    days_of_week=["Wednesday"],
    only_days=[
        "4/10/2024",
        "4/17/2024",
    ],
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Kimbell"],
    fields=["Diamond 1"],
    intended_division="Majors",
    days_of_week=["Wednesday"],
    only_days=[
        "3/6/2024",
        "3/13/2024",
        "3/20/2024",
        "3/27/2024",
        "4/3/2024",
        "4/24/2024",
        "5/1/2024",
        "5/8/2024",
        "5/15/2024",
    ],
    # start_day="3/2/2024",
    # end_day="5/19/2024",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)




##################################################
# Challenger

cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Challenger",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("14:00","16:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Riordan"],
    fields=["Field 1"],
    intended_division="Challenger",
    days_of_week=["Sunday"],
    start_day="3/2/2024",
    end_day="5/19/2024",
    times=[
        ("14:00","16:00"),
    ],
    input=cFrame,
)


##################################################
# Completely erase 4/06 and redo it.

fixDate = "4/6/2024"
cFrame = cFrame[cFrame["Date"] != "2024-04-06"]

# cFrame = add_time_slots(
#     locations=["Paul Goode"],
#     fields=["Practice"],
#     intended_division="Rookie",
#     days_of_week="Saturday",
#     start_day=fixDate,
#     end_day=fixDate,
#     times=[("09:00", "11:30")],
#     input=cFrame,
# )
cFrame = add_time_slots(
    locations=["Larsen"],
    fields=["Field 1"],
    intended_division="Rookie",
    days_of_week=["Saturday"],
    start_day=fixDate,
    end_day=fixDate,
    times=[
        ("09:00", "11:30"),
        ("11:30", "14:00"),
    ],
    input=cFrame,
)
cFrame = add_time_slots(
    locations=["Rossi"],
    fields=["Field 1"],
    intended_division="Rookie",
    days_of_week=["Saturday"],
    start_day=fixDate,
    end_day=fixDate,
    times=[
        ("09:00", "11:30"),
        ("11:30", "14:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Rossi"],
    fields=["Field 1"],
    intended_division="Minors AA",
    days_of_week=["Saturday"],
    start_day=fixDate,
    end_day=fixDate,
    times=[
        ("14:00", "16:30"),
        ("16:30", "19:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Fort Scott"],
    fields=["South Diamond"],
    intended_division="Minors AA",
    days_of_week=["Saturday"],
    start_day=fixDate,
    end_day=fixDate,
    times=[
        ("14:00", "16:30"),
        ("16:30", "19:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Rookie",
    days_of_week=["Saturday"],
    start_day=fixDate,
    end_day=fixDate,
    times=[
        ("14:00", "16:30"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Saturday"],
    start_day=fixDate,
    end_day=fixDate,
    times=[
        ("11:30", "14:00"),
        ("14:00", "16:30"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Saturday"],
    start_day=fixDate,
    end_day=fixDate,
    times=[
        ("11:30", "14:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Fort Scott"],
    fields=["North Diamond"],
    intended_division="Minors AAA",
    days_of_week=["Saturday"],
    start_day=fixDate,
    end_day=fixDate,
    times=[
        ("14:00", "16:30"),
        ("16:30", "19:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Tepper", "Ketcham"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Saturday"],
    start_day=fixDate,
    end_day=fixDate,
    times=[
        ("09:00", "11:30"),
    ],
    input=cFrame,
)

# Change intended first week midweek to only allow Majors
week_one = cFrame["Week_Number"] == "1"
weekdays = ["Monday","Tuesday", "Wednesday", "Thursday", "Friday"]
weekday = cFrame["Day_of_Week"].isin(weekdays)
cFrame.loc[
    (week_one) & (weekday),
    "Intended_Division",
] = "Minors AA"


# Change intended first week midweek to only allow Majors
week_one = cFrame["Week_Number"] == "1"
weekdays = ["Monday","Tuesday", "Wednesday", "Thursday", "Friday"]
weekday = cFrame["Day_of_Week"].isin(weekdays)
ssfields = ["South Sunset - Diamond 1"]
ss = cFrame["Full_Field"].isin(ssfields)
cFrame.loc[
    (week_one) & (weekday) & (ss),
    "Intended_Division",
] = "Minors AAA"

# Change intended first week midweek to only allow Majors
week_one = cFrame["Week_Number"] == "1"
weekdays = ["Monday","Tuesday", "Wednesday", "Thursday", "Friday"]
weekday = cFrame["Day_of_Week"].isin(weekdays)
ssfields = ["South Sunset - Diamond 2"]
ss = cFrame["Full_Field"].isin(ssfields)
cFrame.loc[
    (week_one) & (weekday) & (ss),
    "Intended_Division",
] = "Majors"


# Change intended first week midweek to only allow Majors
week_choice = cFrame["Week_Number"] == "9"
weekdays = ["Wednesday"]
weekday = cFrame["Day_of_Week"].isin(weekdays)
ssfields = ["Kimbell - Diamond 1"]
ss = cFrame["Full_Field"].isin(ssfields)
cFrame.loc[
    (week_choice) & (weekday) & (ss),
    "Intended_Division",
] = "Minors AA"


# Change intended first week midweek to only allow Majors
week_one = cFrame["Week_Number"] == "1"
weekdays = ["Monday","Tuesday", "Wednesday", "Thursday", "Friday"]
kd3 = cFrame["Full_Field"] == "Kimbell - Diamond 3"
weekday = cFrame["Day_of_Week"].isin(weekdays)
cFrame.loc[
    (week_one) & (weekday) & (kd3),
    "Intended_Division",
] = "NONE TOO SMALL"



# Change intended first week midweek to only allow Majors
on_ti  = cFrame["Region"]== "TI"
cFrame.loc[
    (week_one) & (weekday) & (on_ti),
    "Intended_Division",
] = "NONE_DARK"





# ##################################################
# # Cleanup
cFrame.sort_values(by=["Datestamp"], inplace=True, ignore_index=True)

# Add Notes to early opening day slots to avoid scheduling
opening_day = cFrame["Date"] == "2024-03-09"
before_noon_starts = ["08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30"]
before_noon_slots = cFrame["Start"].isin(before_noon_starts)
opening_day_slots = opening_day & before_noon_slots
cFrame.loc[opening_day_slots, "Notes"] = "Opening Day Ceremony"


save_frame(cFrame, "calendar.pkl")
# publish_df_to_gsheet(cFrame)
