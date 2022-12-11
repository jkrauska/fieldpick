from gsheets import publish_df_to_gsheet
from helpers import add_time_slots, fort_scott, tepper_ketcham, weekdays
import pandas as pd
import logging

logging.basicConfig(
    format="%(asctime)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO
)
logger = logging.getLogger()


# Override pandas display settings
pd.set_option("display.max_rows", 500)

# Wrapper function
# FIXME: Can this go in helpers.py?


cFrame = pd.DataFrame()


##################################################
### Fort Scott
# Saturdays 3/11 -- 5/27 (every other week situation)
cFrame = add_time_slots(
    fields=fort_scott,
    days_of_week=["Saturday"],
    only_days=[
        "3/11/2023",
        "3/25/2023",
        "4/8/2023",
        "4/22/2023",
        "5/6/2023",
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
    times=[("17:00", "20:30")],
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
    days_of_week=weekdays,
    start_day="3/13/2023",
    end_day="5/9/2023",
    times=[("17:00", "19:30")],
    input=cFrame,
)

##################################################
# Cleanup
cFrame.sort_values(by=["Datestamp"], inplace=True, ignore_index=True)

print(cFrame)

save_file = "data/calendar.pkl"
logger.info(f"Saving to disk: {save_file}")
cFrame.to_pickle(save_file)


logger.info("Publishing to Google Sheets")
publish_df_to_gsheet(cFrame)
