import pandas as pd
import logging
import random
from inputs import division_info

logging.basicConfig(
    format="%(asctime)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO
)
logger = logging.getLogger()

tFrame = pd.DataFrame()

for division in division_info:
    logger.info(f"Generating {division_info[division]['teams']} teams for {division}")
    for i in range(division_info[division]["teams"]):
        new_row = pd.DataFrame(
            {
                "Division": division,
                "Team_Number": i + 1,
                "Team": f"Team {i + 1}",
                "Team_Full": f"{division} Team {i + 1}",
            }, index=[0])

        tFrame = pd.concat([tFrame, new_row],
            ignore_index=True,
        )

save_file = "data/teams.pkl"
logger.info(f"Saving to disk: {save_file}")
tFrame.to_pickle(save_file)