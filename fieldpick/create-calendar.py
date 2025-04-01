from helpers import add_time_slots, fort_scott, tepper_ketcham, tuesday_thursday
from datetime import datetime
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

special_schedule_dates = [
    "4/5/2025",  # Giants Saturday
    "4/19/2025",  # Easter Saturday
]

# Datetime conversion for blackouts
special_schedule_days = [datetime.strptime(
    date, "%m/%d/%Y") for date in special_schedule_dates]


##################################################
# Tee Ball

cFrame = add_time_slots(
    locations=["Aptos"],
    fields=["Field 1"],
    intended_division="Tee Ball",
    days_of_week="Saturday",
    start_day="3/1/2025",
    end_day="5/18/2025",
    times=[("09:00", "10:30")],
    input=cFrame,
    blackout_days=special_schedule_days,
)

# tee 1.5h on Saturdays
cFrame = add_time_slots(
    locations=["Larsen"],
    fields=["Field 1"],
    intended_division="Tee Ball",
    days_of_week=["Saturday"],
    start_day="3/1/2025",
    end_day="5/18/2025",
    times=[
        ("09:00", "10:30"),
        ("10:30", "12:00"),
        ("12:00", "13:30"),
        ("13:30", "15:00"),
    ],
    input=cFrame,
    blackout_days=special_schedule_days,
)

cFrame = add_time_slots(
    locations=["Paul Goode"],
    fields=["Practice"],
    intended_division="Tee Ball",
    days_of_week=["Saturday"],
    start_day="3/1/2025",
    end_day="5/18/2025",
    times=[
        ("11:00", "12:30"),
        ("12:30", "14:00"),
    ],
    input=cFrame,
)


##################################################
# Lower Farm
cFrame = add_time_slots(
    locations=["Larsen"],
    fields=["Field 1"],
    intended_division="Lower Farm",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/18/2025",
    times=[
        ("09:00", "11:00"),
        ("11:00", "13:00"),
        ("13:00", "15:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Rossi"],
    fields=["Field 1"],
    intended_division="Lower Farm",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/18/2025",
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
    start_day="3/1/2025",
    end_day="5/18/2025",
    times=[
        ("08:00", "10:00"),
        ("10:00", "12:00"),
        ("12:00", "14:00"),
    ],  # 2 h slots
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Fort Scott"],
    fields=["South Diamond"],
    intended_division="Upper Farm",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/18/2025",
    times=[
        ("08:00", "10:00"),
        ("10:00", "12:00"),
        ("12:00", "14:00"),
    ],  # 2 h slots
    input=cFrame,
)

##################################################
# Rookie
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Rookie",
    days_of_week=["Saturday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[("11:30", "14:00")],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Rookie",
    days_of_week=["Saturday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[("14:00", "16:30")],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Aptos"],
    fields=["Field 1"],
    intended_division="Rookie",
    days_of_week=["Saturday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("10:30", "13:00"),
    ],
    input=cFrame,
    blackout_days=special_schedule_days,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Rookie",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("11:30", "14:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Sunset Rec"],
    fields=["Diamond"],
    intended_division="Rookie",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("11:30", "14:00"),
    ],
    input=cFrame,
)

# Thurs
cFrame = add_time_slots(
    locations=["Fort Scott"],
    fields=["South Diamond"],
    intended_division="Rookie",
    days_of_week=["Thursday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Balboa"],
    fields=["D2"],
    intended_division="Rookie",
    days_of_week=["Thursday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

# Friday
cFrame = add_time_slots(
    locations=["Fort Scott"],
    fields=["South Diamond"],
    intended_division="Rookie",
    days_of_week=["Friday"],
    start_day="3/10/2025",
    end_day="5/1/2025",

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
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[("14:00", "16:30")],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Aptos"],
    fields=["Field 1"],
    intended_division="Minors AA",
    days_of_week=["Saturday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("13:00", "15:30"),
    ],
    input=cFrame,
)

# Sunday
cFrame = add_time_slots(
    locations=["Sunset Rec"],
    fields=["Diamond"],
    intended_division="Minors AA",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[("09:00", "11:30")],
    input=cFrame,
)


cFrame = add_time_slots(
    locations=["West Sunset"],
    fields=["Field 3"],
    intended_division="Minors AA",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("11:30", "14:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Minors AA",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("14:00", "16:30"),
    ],
    input=cFrame,
)

# Weds and Thurs inherited from Rookie

# Thursday

cFrame = add_time_slots(
    locations=["Fort Scott"],
    fields=["North Diamond"],
    intended_division="Minors AA",
    days_of_week=["Thursday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["South Sunset"],
    fields=["Diamond 1"],
    intended_division="Minors AA",
    days_of_week=["Thursday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

# Friday
cFrame = add_time_slots(
    locations=["South Sunset"],
    fields=["Diamond 2"],
    intended_division="Minors AA",
    days_of_week=["Friday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

##################################################
# AAA Minors

# Saturday
cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Saturday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("11:30", "14:00"),
    ],
    input=cFrame,
    blackout_days=special_schedule_days,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Saturday"],
    start_day="3/9/2025",  # Start of Daylight Saving Time
    end_day="5/2/2025",
    times=[
        ("16:30", "19:00"),
    ],
    input=cFrame,
)

# Sunday
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("11:30", "14:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("09:00", "11:30"),
    ],
    input=cFrame,
)


cFrame = add_time_slots(
    locations=["West Sunset"],
    fields=["Field 3"],
    intended_division="Minors AAA",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("09:00", "11:30"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Thursday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Thursday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Fort Scott"],
    fields=["North Diamond"],
    intended_division="Minors AAA",
    days_of_week=["Friday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

##################################################
# Majors
# Sat, Sun, Tue, Wed, Fri

# Sat
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Saturday"],
    start_day="3/8/2025",  # Skip Week 1 so AAA can have the slot
    end_day="5/2/2025",
    times=[
        ("09:00", "11:30"),
    ],
    input=cFrame,
    blackout_days=special_schedule_days,
)

cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Saturday"],
    start_day="3/9/2025",  # Start of Daylight Saving Time
    end_day="5/2/2025",
    times=[
        ("16:30", "19:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Saturday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[("09:00", "11:30")],
    input=cFrame,
)

# Sunday
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("09:00", "11:30"),
        ("16:00", "18:30"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Sunday"],
    start_day="3/9/2025",  # Start of Daylight Saving Time
    end_day="5/2/2025",
    times=[
        ("16:30", "19:00"),
    ],
    input=cFrame,
)

# Tuesday
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Tuesday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Tuesday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

# Wednesday
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Wednesday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Ketcham"],
    fields=["Field 1"],
    intended_division="Majors",
    days_of_week=["Wednesday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)


# Friday
cFrame = add_time_slots(
    locations=["South Sunset"],
    fields=["Diamond 1"],
    intended_division="Majors",
    days_of_week=["Friday"],
    start_day="3/10/2025",
    end_day="5/2/2025",
    times=[
        ("17:30", "20:00"),
    ],
    input=cFrame,
)

##################################################
# Juniors

cFrame = add_time_slots(
    locations=["Moscone"],
    fields=["D4"],
    intended_division="Juniors",
    days_of_week=["Saturday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("09:00", "12:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Paul Goode"],
    fields=["Main"],
    intended_division="Juniors",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("09:00", "12:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["West Sunset"],
    fields=["Field 1"],
    intended_division="Juniors",
    days_of_week=["Sunday"],
    start_day="3/1/2025",
    end_day="5/2/2025",
    times=[
        ("09:00", "12:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["McCoppin"],
    fields=["Field 1"],
    intended_division="Juniors",
    days_of_week=["Tuesday", "Wednesday"],
    start_day="3/9/2025",
    end_day="5/2/2025",
    times=[
        ("17:00", "20:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Crocker Amazon"],
    fields=["D2"],
    intended_division="Juniors",
    days_of_week=["Wednesday"],
    start_day="3/9/2025",
    end_day="5/2/2025",
    times=[
        ("17:00", "20:00"),
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
    start_day="3/8/2025",
    end_day="5/18/2025",
    times=[
        ("14:00", "16:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Riordan"],
    fields=["Field 1"],
    intended_division="Challenger",
    days_of_week=["Sunday"],
    start_day="3/8/2025",
    end_day="5/18/2025",
    times=[
        ("14:00", "16:00"),
    ],
    input=cFrame,
)

# Special Schedules (Tentative)

# - Games start for ALL DIVISIONS on Sat 3/1/25
# - NO GAMES ALL DIVISIONS Sunday 3/2/25 before 1:00 PM - Opening Day ceremony
#     This is done by adding notes to early opening day slots, below
# - NO GAMES TB-JR Sunday 4/6/25 - Giants Day
#     This is done immediately below
# - NO GAMES ALL DIVISIONS (TB-JR+Challenger) Sunday 4/20/25 - Easter Sunday
#     This is done immediately below
# - NO GAMES Challenger division only Sunday 5/11/25 - Mother’s Day
#     This is done in assign_challenger.py

cFrame = cFrame[cFrame["Date"] != "2025-04-20"]  # No games Easter Sunday

giants_day = "04/06/2025"

# No games Giants Sunday, except Challenger, added back here:
cFrame = cFrame[cFrame["Date"] != "2025-04-06"]

cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Challenger",
    days_of_week=["Sunday"],
    start_day=giants_day,
    end_day=giants_day,
    times=[
        ("14:00", "16:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    locations=["Riordan"],
    fields=["Field 1"],
    intended_division="Challenger",
    days_of_week=["Sunday"],
    start_day=giants_day,
    end_day=giants_day,
    times=[
        ("14:00", "16:00"),
    ],
    input=cFrame,
)

# Special schedule for Giants Saturday and Easter Saturday


for special_schedule_date in special_schedule_dates:
    cFrame = add_time_slots(
        locations=["Tepper"],
        fields=["Field 1"],
        intended_division="Minors AAA",
        days_of_week=["Saturday"],
        start_day=special_schedule_date,
        end_day=special_schedule_date,
        times=[
            ("09:00", "11:30"),
        ],
        input=cFrame,
    )

    cFrame = add_time_slots(
        locations=["Ketcham"],
        fields=["Field 1"],
        intended_division="Rookie",
        days_of_week=["Saturday"],
        start_day=special_schedule_date,
        end_day=special_schedule_date,
        times=[
            ("11:30", "14:00"),
        ],
        input=cFrame,
    )

    cFrame = add_time_slots(
        locations=["Larsen"],
        fields=["Field 1"],
        intended_division="Lower Farm",
        days_of_week=["Saturday"],
        start_day=special_schedule_date,
        end_day=special_schedule_date,
        times=[
            ("09:00", "11:00"),
            ("11:00", "13:00"),
        ],
        input=cFrame,
    )

    cFrame = add_time_slots(
        locations=["Larsen"],
        fields=["Field 1"],
        intended_division="Upper Farm",
        days_of_week=["Saturday"],
        start_day=special_schedule_date,
        end_day=special_schedule_date,
        times=[
            ("13:00", "15:00"),
        ],
        input=cFrame,
    )

    cFrame = add_time_slots(
        locations=["Aptos"],
        fields=["Field 1"],
        intended_division="Upper Farm",
        days_of_week=["Saturday"],
        start_day=special_schedule_date,
        end_day=special_schedule_date,
        times=[
            ("09:00", "11:00"),
            ("11:00", "13:00"),
        ],
        input=cFrame,
    )

# Give AAA an extra slot on opening day, because they lose 3 opening
# weekend slots to the opening day ceremony and one to darkness
cFrame = add_time_slots(
    locations=["Tepper"],
    fields=["Field 1"],
    intended_division="Minors AAA",
    days_of_week=["Saturday"],
    start_day="3/1/2025",  # Skip Week 1 so AAA can have the slot
    end_day="3/1/2025",
    times=[
        ("09:00", "11:30"),
    ],
    input=cFrame,
    blackout_days=special_schedule_days,
)

# Give Rookie an extra Tepper slot so every team can have two games there.

# Change the Sunday, March 16 11:30-14:00 Tepper game from AAA to Rookie
cFrame.loc[
    (cFrame["Date"] == "2025-03-16") & 
    (cFrame["Start"] == "11:30") & 
    (cFrame["End"] == "14:00") & 
    (cFrame["Location"] == "Tepper") & 
    (cFrame["Field"] == "Field 1"), 
    "Intended_Division"
] = "Rookie"

# Change the Sunday, March 16 11:30-14:00 Ketcham game from Rookie to AAA
cFrame.loc[
    (cFrame["Date"] == "2025-03-16") & 
    (cFrame["Start"] == "11:30") & 
    (cFrame["End"] == "14:00") & 
    (cFrame["Location"] == "Ketcham") & 
    (cFrame["Field"] == "Field 1"), 
    "Intended_Division"
] = "Minors AAA"

# Change the Sunday, March 23 11:30-14:00 Tepper game from its current division to AA
cFrame.loc[
    (cFrame["Date"] == "2025-03-23") & 
    (cFrame["Start"] == "11:30") & 
    (cFrame["Location"] == "Tepper") & 
    (cFrame["Field"] == "Field 1"), 
    "Intended_Division"
] = "Minors AA"

# Change the Sunday, March 23 14:00-16:30 Ketcham game from its current division to AAA
cFrame.loc[
    (cFrame["Date"] == "2025-03-23") & 
    (cFrame["Start"] == "14:00") & 
    (cFrame["Location"] == "Ketcham") & 
    (cFrame["Field"] == "Field 1"), 
    "Intended_Division"
] = "Minors AAA"

# ##################################################
# # Cleanup
cFrame.sort_values(by=["Datestamp"], inplace=True, ignore_index=True)

# Add Notes to early opening day slots to avoid scheduling
opening_day = cFrame["Date"] == "2025-03-02"
early_starts = [
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30"]
early_slots = cFrame["Start"].isin(early_starts)
opening_day_slots = opening_day & early_slots
cFrame.loc[opening_day_slots, "Notes"] = "Opening Day Ceremony"

save_frame(cFrame, "calendar.pkl")
# publish_df_to_gsheet(cFrame)
