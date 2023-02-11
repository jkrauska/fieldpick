
import pandas as pd
import logging
from helpers import add_time_slots, tepper_ketcham, tuesday_thursday
from frametools import save_frame
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
logger.info(f"Loaded {len(cFrame)} slots")

##################################################
### Tepper/Ketcham

# cFrame = add_time_slots(
#     fields=tepper_ketcham,
#     days_of_week=["Saturday", "Sunday"],
#     start_day="3/11/2023",
#     end_day="3/12/2023",
#     times=[("16:30", "19:00")],
#     input=cFrame,
# )

# cFrame = add_time_slots(
#     fields=tepper_ketcham,
#     days_of_week=["Saturday", "Sunday"],
#     start_day="3/11/2023",
#     end_day="6/5/2023",
#     times=[("09:00", "11:30"), ("11:30", "14:00"), ("14:00", "16:30")],
#     input=cFrame,
# )


# cFrame = add_time_slots(
#     fields=tepper_ketcham,
#     days_of_week=["Saturday", "Sunday"],
#     start_day="5/28/2023",
#     end_day="6/4/2023",
#     times=[("16:30", "19:00")],
#     input=cFrame,
# )

# # Tues-Friday After main season
# cFrame = add_time_slots(
#     fields=tepper_ketcham,
#     # days_of_week=weekdays,
#     days_of_week=tuesday_thursday,
#     start_day="5/10/2023",
#     end_day="5/28/2023",
#     times=[("17:00", "19:30")],
#     input=cFrame,
# )


### FIX
# Delete a known bad slot.
# cFrame.drop(325, inplace=True)
# cFrame.drop(329, inplace=True)

cFrame.sort_values(by=["Datestamp"], inplace=True)

save_frame(cFrame, "calendar.pkl")

# publish_df_to_gsheet(cFrame, worksheet_name="New Full Schedule")
