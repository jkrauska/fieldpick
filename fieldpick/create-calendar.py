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
### Fort Scott
# Saturdays 3/11 -- 5/27 (every other week situation)
cFrame = add_time_slots(
    fields="Ft. Scott - North",
    days_of_week=["Saturday", "Sunday"],
    only_days=[
        "3/5/2023",
        "3/11/2023",
        "3/19/2023",
        "3/25/2023",
        "4/2/2023",
        "4/8/2023",
        "4/16/2023",
        "4/22/2023",
        "4/30/2023",
        "5/7/2023",
        "5/14/2023",
        "5/20/2023",
        "5/27/2023",
    ],
    times=[("09:00", "11:30"), ("11:30", "14:00")],
    input=cFrame,
)

cFrame = add_time_slots(
    fields="Ft. Scott - South",
    days_of_week=["Saturday", "Sunday"],
    only_days=[
        "3/5/2023",
        "3/11/2023",
        "3/19/2023",
        "3/25/2023",
        "4/2/2023",
        "4/8/2023",
        "4/16/2023",
        "4/22/2023",
        "4/30/2023",
        "5/7/2023",
        "5/14/2023",
        "5/20/2023",
        "5/27/2023",
    ],
    times=[("09:30", "11:30"), ("12:00", "14:00")],
    input=cFrame,
)


# Tuesday/Thursday
cFrame = add_time_slots(
    fields=fort_scott,  ## FIXME: BOTH fields on just FSN?
    days_of_week=["Tuesday", "Thursday"],
    start_day="3/14/2023",
    end_day="5/30/2023",
    times=[("17:00", "19:30")],
    input=cFrame,
)

##################################################
### Tepper/Ketcham

cFrame = add_time_slots(
    fields=tepper_ketcham,
    days_of_week=["Saturday"],
    start_day="3/4/2023",
    end_day="5/5/2023",
    times=[("09:00", "11:30"), ("11:30", "14:00"), ("14:00", "16:30")],
    input=cFrame,
)

cFrame = add_time_slots(
    fields=tepper_ketcham,
    days_of_week=["Sunday"],
    start_day="3/4/2023",
    end_day="5/5/2023",
    times=[("09:00", "11:30"), ("11:30", "14:00"), ("14:00", "16:30")],
    input=cFrame,
)

# Monday-Friday after DST change (3/12/23)
# Sunset 19:15 on 3/13/23
cFrame = add_time_slots(
    fields=tepper_ketcham,
    # days_of_week=weekdays,
    days_of_week=tuesday_thursday,
    start_day="3/13/2023",
    end_day="5/9/2023",
    times=[("17:00", "19:30")],
    input=cFrame,
)

##################################################
## Paul Goode
cFrame = add_time_slots(
    fields=["Paul Goode Practice"],
    days_of_week="Saturday",
    start_day="3/11/2023",
    end_day="5/27/2023",
    times=[("11:00", "12:30"), ("12:30", "14:00")],
    input=cFrame,
)

# carved for 2h on Sundays
cFrame = add_time_slots(
    fields="Paul Goode Practice",
    days_of_week="Sunday",
    start_day="2/25/2023",
    end_day="5/27/2023",
    times=[("09:00", "11:00")],
    input=cFrame,
)

cFrame = add_time_slots(
    fields="Paul Goode Main",
    days_of_week="Sunday",
    start_day="2/25/2023",
    end_day="5/27/2023",
    times=[("15:00", "18:00")],
    input=cFrame,
)
##################################################
# RecPark Weekdays

# cFrame = add_time_slots(
#     fields=["Kimbell D1 NW", "Kimbell D2 SE", "Kimbell D3 SW"],
#     days_of_week="Wednesday",
#     start_day="3/8/2023",
#     end_day="5/27/2023",
#     times=[("17:30", "20:00")],
#     input=cFrame,
# )

cFrame = add_time_slots(
    fields=["Kimbell D1 NW", "Kimbell D2 SE", "Kimbell D3 SW"],
    days_of_week="Wednesday",
    start_day="3/8/2023",
    end_day="5/27/2023",
    times=[("17:30", "20:00")],
    input=cFrame,
)


cFrame = add_time_slots(
    fields=["McCoppin"],
    days_of_week="Tuesday",
    start_day="3/7/2023",
    end_day="5/27/2023",
    times=[("17:30", "20:30")],  # needs to be hard set to 3h to avoid being used by Rookie/Minors...
    input=cFrame,
)

cFrame = add_time_slots(
    fields=["South Sunset D2 South"],
    days_of_week=["Tuesday", "Thursday", "Friday"],
    start_day="3/7/2023",
    end_day="5/27/2023",
    times=[("17:30", "20:00")],
    input=cFrame,
)

cFrame = add_time_slots(
    fields=["South Sunset D1 North"],
    days_of_week=["Friday"],
    start_day="3/7/2023",
    end_day="5/27/2023",
    times=[("17:30", "20:00")],
    input=cFrame,
)

##################################################
# RecPark Weekends

# tee 1.5h on Saturdays
cFrame = add_time_slots(
    fields=["Larsen"],
    days_of_week=["Saturday"],
    start_day="3/4/2023",
    end_day="5/22/2023",
    times=[
        ("09:00", "10:30"),
        ("10:30", "12:00"),
        ("12:00", "13:30"),
        ("13:30", "15:00"),
        ("15:00", "16:30"),
    ],
    input=cFrame,
)

# farm 2h on sundays
cFrame = add_time_slots(
    fields=["Larsen", "Christopher"],
    days_of_week=["Sunday"],
    start_day="3/4/2023",
    end_day="5/22/2023",
    times=[
        ("09:00", "11:00"),
        ("11:00", "13:00"),
        ("13:00", "15:00"),
        ("15:00", "17:00"),
    ],
    input=cFrame,
)


# 2h slots (farm)
cFrame = add_time_slots(
    fields=["Rossi Park #1"],
    days_of_week=["Sunday"],
    start_day="3/4/2023",
    end_day="5/22/2023",
    times=[
        ("09:00", "11:00"),
        ("11:00", "13:00"),
    ],
    input=cFrame,
)

# 2.5h slots (rookie)
cFrame = add_time_slots(
    fields=["Rossi Park #1"],
    days_of_week=["Saturday", "Sunday"],
    start_day="3/4/2023",
    end_day="5/22/2023",
    times=[
        ("13:00", "15:30"),  # 2h
        ("15:30", "18:00"),  # 2.5h
    ],
    input=cFrame,
)


# Large fields (Juniors)
cFrame = add_time_slots(
    fields=["Balboa - Sweeney"],
    days_of_week=["Saturday"],
    start_day="3/4/2023",
    end_day="5/22/2023",
    times=[
        ("09:00", "12:00"),
        ("12:00", "15:00"),
    ],
    input=cFrame,
)

cFrame = add_time_slots(
    fields=["McCoppin"],
    days_of_week=["Sunday"],
    start_day="3/4/2023",
    end_day="5/22/2023",
    times=[
        ("09:00", "12:00"),
    ],
    input=cFrame,
)

# Challenger @ Riordan
cFrame = add_time_slots(
    fields=["Riordan"],
    days_of_week=["Sunday"],
    only_days=[
        "3/5/2023",
        "3/19/2023",
        "3/26/2023",
        "4/2/2023",
        "4/9/2023",
        "4/16/2023",
        "4/23/2023",
        "4/30/2023",
        "5/7/2023",
        "5/14/2023",
        "5/21/2023",
    ],
    times=[
        ("13:30", "16:30"),
    ],
    input=cFrame,
)

##################################################
# Cleanup
cFrame.sort_values(by=["Datestamp"], inplace=True, ignore_index=True)

# print(cFrame)


cFrame.loc[cFrame["Datestamp"] < "2023-03-04 14:00", "Notes"] = "Opening Day Ceremony"


save_frame(cFrame, "calendar.pkl")
# publish_df_to_gsheet(cFrame)
