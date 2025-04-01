import pandas as pd
import logging
from inputs import division_info
from frametools import save_frame
from helpers import sports_connect_division_names

logging.basicConfig(
    format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO)
logger = logging.getLogger()

tFrame = pd.DataFrame()

"""
TB: TB_01 - TB_14
LF: LF_01 - LF_12
UF: UF_01 - UF_12
Rookie: Rookie_AL_01 - Rookie_AL_05, Rookie_NL_01 - Rookie_NL_05
AA: AA_AL_01 - AA_AL_05, AA_NL_01 - AA_NL_05
AAA: AAA_AL_01 - AAA_AL_05, AAA_NL_01 - AAA_NL_05
Majors: Majors_AL_01 - Majors_AL_05, Majors_NL_01 - Majors_NL_05
Juniors: Juniors_01 -Juniors_06
Challenger: Challenger_01 - Challenger_04

"""


def sports_connect_team_numbers_and_names(division):
    all_teams = division_info[division]["teams"]
    if division_info[division].get("al_nl_split", False):
        half_teams = int(all_teams / 2)
        for i in range(half_teams):
            yield (i + 1, f"{sports_connect_division_names[division]}_AL_{i + 1:02d}")
        for i in range(half_teams, all_teams):
            yield (i + 1, f"{sports_connect_division_names[division]}_NL_{i + 1:02d}")
    else:
        for i in range(all_teams):
            yield (i + 1, f"{sports_connect_division_names[division]}_{i + 1:02d}")


for division in division_info:
    logger.info(f"Division: {division}")
    logger.info(
        f"Generating {
            division_info[division]['teams']} teams for {division}")
    for team_number, team_name in sports_connect_team_numbers_and_names(
            division):
        new_row = pd.DataFrame(
            {
                "Division": division,
                "Team_Number": team_number,
                "Team": team_name,
                "Team_Full": f"{division} Team {team_number}",
            },
            index=[0],
        )

        tFrame = pd.concat(
            [tFrame, new_row],
            ignore_index=True,
        )


save_frame(tFrame, "teams.pkl")
