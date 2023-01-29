import pandas as pd
import logging
import sys
from inputs import division_info
from frametools import list_teams_for_division, weeks_in_season, save_frame, score_frame, clear_division, reserve_slots
from faceoffs import faceoffs_repeated
from gsheets import publish_df_to_gsheet


from random import shuffle, seed

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


# Block off for Challenger
cFrame.update(reserve_slots(cFrame, day_of_week="Sunday", field="Riordan", start="13:30", division="Challenger"))
cFrame.update(reserve_slots(cFrame, day_of_week="Sunday", field="Tepper", start="14:00", division="Challenger"))
cFrame.update(reserve_slots(cFrame, day_of_week="Sunday", field="McCoppin", start="09:00", division="Challenger", date="2023-03-12"))


# Main loop

# Iterate over each division
for division in division_info.keys():

    random_seed = division_info[division].get("random_seed", 0)
    max_loops = division_info[division].get("max_loops", 1)

    loop_count = 0
    best_score = 999
    best_seed = 0

    while loop_count <= max_loops:
        seed(random_seed)  # Set random seed for this division

        teams = list_teams_for_division(division, tFrame)
        faceoffs = faceoffs_repeated(teams)
        logger.debug(f"Faceoffs for {division}: {faceoffs}")
        logger.info("#" * 80)
        logger.info(f"Processing {division} with {len(teams)} teams")

        # Per division preferences
        weekly_games_to_schedule = division_info[division].get("games_per_week", 0)
        if weekly_games_to_schedule == 0:
            logger.warning(f"\tNo games to schedule for {division}")
            loop_count += 1

            continue

        preferred_fields = division_info[division].get("preferred_fields", [None])
        preferred_days = division_info[division].get("preferred_days", [None])

        logger.info(f"\tPreferred days: {preferred_days}")
        logger.info(f"\tPreferred fields: {preferred_fields}")

        skip_weeks = division_info[division].get("skip_weeks", [])
        time_length = division_info[division].get("time_length", None)

        for week in weeks_in_season(cFrame):
            games_to_schedule = weekly_games_to_schedule
            if week in skip_weeks:
                logger.info(f"\t⤵ Skipping Week {week}")
                continue
            logger.info(f"\tProcessing {division} -- Week {week} -- Games to schedule: {games_to_schedule} -- {len(cFrame)} slots")

            # Convert preferred_days to nested list if needed
            if isinstance(preferred_days[0], str):
                preferred_days = [preferred_days]

            for preferred_days_set in preferred_days:
                if isinstance(preferred_fields, str):
                    preferred_fields = [preferred_fields]

                for preferred_fields_set in preferred_fields:
                    if games_to_schedule == 0:
                        logger.info("\t\t✅ No more games to schedule")
                        break

                    # Filter down selections to preferred days and fields, etc.
                    cs = cFrame.query("Week_Number == @week")
                    if preferred_days_set:
                        # logger.info(f"Set constraints: {preferred_days_set}")
                        cs = cs.query("Day_of_Week in @preferred_days_set")
                    if preferred_fields_set and preferred_fields_set != [None]:
                        # logger.info(f"Set constraints: {preferred_fields_set}")
                        cs = cs.query("Field in @preferred_fields_set")
                    if time_length:
                        # logger.info(f"Set constraints: {time_length}")
                        cs = cs.query("Time_Length == @time_length")

                    # Special case to put Challenger games
                    if division == "Challenger":
                        if "Riordan" in preferred_fields_set:
                            cs = cs.query("Start == '13:30'")
                        elif "Tepper" in preferred_fields_set:
                            cs = cs.query("Start == '14:00'")
                        elif "McCoppin" in preferred_fields_set:
                            cs = cs.query("Start == '09:00'")

                    candidate_slots = pd.isnull(cs["Home_Team"]).index.tolist()
                    shuffle(candidate_slots)

                    logger.info(f"\tFound {len(candidate_slots)} candidate slots: {candidate_slots}")

                    # Try each candidate slot
                    while len(candidate_slots) > 0:
                        slot = candidate_slots.pop(0)

                        if pd.isnull(cFrame.loc[slot, "Home_Team"]):
                            logger.debug(f"\t\tSlot {slot} is available")

                            # Grab the next faceoff
                            if faceoffs:
                                faceoff = faceoffs.pop(0)
                                home_team = faceoff[0]
                                away_team = faceoff[1]
                            else:
                                logger.info("\t\tNo more faceoffs to process")
                                break

                            # Assign the teams to the slot
                            cFrame.loc[slot, "Division"] = division
                            cFrame.loc[slot, "Home_Team"] = home_team
                            cFrame.loc[slot, "Away_Team"] = away_team

                            games_to_schedule -= 1
                            logger.info(f"\t\tPlaced {faceoff} in slot {slot} - Games left to schedule: {games_to_schedule}")
                            if games_to_schedule == 0:
                                logger.info("\t\t✅ No more games to schedule")
                                break

                        else:
                            logger.debug(f"\t\tSlot {slot} is unavailable")
                            continue

            if games_to_schedule > 0:
                logger.warning(f"\t\t❌ Unable to schedule {games_to_schedule} games for {division} in week {week}")

        # End of division loop

        # Score the results
        field_score = score_frame(cFrame, division, "Field")
        start_score = score_frame(cFrame, division, "Start")

        total_score = field_score + start_score

        # Track best score
        if total_score < best_score:
            best_score = total_score
            best_seed = random_seed

        logger.info(f"SCORES FOR {division} on {random_seed}:{total_score:0.3f}  Best: {best_seed}:{best_score:0.3f}")

        loop_count += 1

        logger.info(f"Loop {loop_count} of {max_loops}")

        # Annoyed about this logic vs the while loop
        if max_loops == 1:
            # Not looping, so just exit
            logger.info(f"Best SCORE for {division} is {best_seed}:{best_score:0.3f}")
            break
        elif loop_count == max_loops:
            # intentionally set to best result for last run
            logger.info(f"RERUNNING Best SCORE for {division} \tis {best_score:0.3f} with seed {best_seed}")
            random_seed = best_seed
            cFrame = clear_division(division, cFrame)
        elif loop_count > max_loops:
            # We're done
            break

        else:
            # otherwise just increase seed
            random_seed += 1
            cFrame = clear_division(division, cFrame)

    # break


save_frame(cFrame, "calendar.pkl")
publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")
