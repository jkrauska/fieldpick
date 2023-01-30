import pandas as pd
import logging
from inputs import division_info
from frametools import list_teams_for_division, weeks_in_season, save_frame, score_frame, reserve_slots, check_consecutive
from faceoffs import faceoffs_repeated
from gsheets import publish_df_to_gsheet
from datetime import datetime
from helpers import tepper_ketcham


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
cFrame.update(
    reserve_slots(cFrame, day_of_week="Sunday", field="McCoppin", start="09:00", division="Challenger", date="2023-03-12")
)


# Main loop

# Iterate over each division
for division in division_info.keys():

    random_seed = division_info[division].get("random_seed", 0)
    max_loops = division_info[division].get("max_loops", 1)

    loop_count = 0
    best_score = 999
    best_seed = 0
    t0 = datetime.now()

    while loop_count <= max_loops:
        seed(random_seed)  # Set random seed for this division

        backup_frame = cFrame.copy()  # Save a copy of the calendar in case we need to revert

        teams = list_teams_for_division(division, tFrame)
        faceoffs = faceoffs_repeated(teams, games=200)  # Make sure we have enough faceoffs to work with
        logger.debug(f"Faceoffs for {division}: {faceoffs}")
        logger.info("#" * 80)
        logger.info(f"Processing {division} with {len(teams)} teams")

        # Per division preferences
        if "games_per_week_pattern" in division_info[division]:
            games_per_week_pattern = division_info[division].get("games_per_week_pattern")
        else:
            games_per_week_pattern = None
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
        midweek_start = division_info[division].get("midweek_start", None)
        time_length = division_info[division].get("time_length", None)
        denied_fields = division_info[division].get("denied_fields", [])
        dedicated_ti_weekend = division_info[division].get("dedicated_ti_weekend", None)

        for week in weeks_in_season(cFrame):

            # Check total slots available this week
            query_builder = "Week_Number == @week"  # checks notes are Null
            query_builder += " and Notes != Notes"  # notes are empty
            query_builder += " and Division != Division"  # division is empty
            query_builder += " and Time_Length == @time_length"

            actually_available_slots = len(cFrame.query(query_builder))
            logger.info(f"\tActually available slots: {division} w:{week}  s:{actually_available_slots}")

            # See if we're in a changing pattern schedule
            if games_per_week_pattern:
                games_to_schedule = games_per_week_pattern[int(week) - 1]
            else:
                games_to_schedule = weekly_games_to_schedule

            if week in skip_weeks:
                logger.info(f"\t⤵ Skipping Week {week}")
                continue

            if actually_available_slots < games_to_schedule:
                logger.warning(
                    f"\t⚠️ Less slots available than games to schedule {division} {week} ({actually_available_slots} < {games_to_schedule})"
                )

            if actually_available_slots < games_to_schedule / 3:
                logger.warning(
                    f"\t⚠️ Less than 1/3 slots available than games to schedule {division} {week} ({actually_available_slots} < {games_to_schedule})"
                )

            logger.info(
                f"\tProcessing {division} -- Week {week} -- Games to schedule: {games_to_schedule} -- {len(cFrame)} slots"
            )

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

                    query_builder = "Week_Number == @week"  # checks notes are Null
                    query_builder += " and Notes != Notes"  # notes are empty
                    query_builder += " and Division != Division"  # division is empty

                    # Add constraints to query if we have them
                    if preferred_days_set:
                        query_builder += " and Day_of_Week in @preferred_days_set"
                    if preferred_fields_set and preferred_fields_set != [None]:
                        query_builder += " and Field in @preferred_fields_set"
                    if time_length:
                        query_builder += " and Time_Length == @time_length"

                    cs = cFrame.query(query_builder)

                    # FIXME Block Midweek here before 3/14/23
                    if midweek_start and int(week) < int(midweek_start):
                        cs = cs.query("Day_of_Week != 'Monday'")
                        cs = cs.query("Day_of_Week != 'Tuesday'")
                        cs = cs.query("Day_of_Week != 'Wednesday'")
                        cs = cs.query("Day_of_Week != 'Thursday'")
                        cs = cs.query("Day_of_Week != 'Friday'")

                    # Block things like Kimbell D3 from bigger kids
                    if denied_fields:
                        cs = cs.query("Field not in @denied_fields")

                    # Block dedicated TI weekend
                    if dedicated_ti_weekend:
                        if int(week) == int(dedicated_ti_weekend):
                            cs = cs.query("Field in @tepper_ketcham")
                        else:
                            cs = cs.query("Field not in @tepper_ketcham")

                    candidate_slots = pd.isnull(cs["Home_Team"]).index.tolist()

                    # Shuffle the candidate slots
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
                            row = cFrame.loc[slot]

                            games_to_schedule -= 1
                            logger.info(
                                f"\t\tPlaced {faceoff} in slot {slot} at {row.Field} {row.Day_of_Week} {row.Datestamp} - Games left:{games_to_schedule}"
                            )
                            if games_to_schedule == 0:
                                logger.info("\t\t✅ No more games to schedule")
                                break

                        else:
                            logger.debug(f"\t\tSlot {slot} is unavailable")
                            continue

            if games_to_schedule > 0:
                logger.warning(f"\t\t❌ Unable to schedule {games_to_schedule} games for {division} in week {week}")

        window = 100
        if loop_count % window == 0:
            logger.info(f"Loop {loop_count} of {max_loops}")
            t1 = datetime.now()
            logger.info(f"Elapsed time: {t1 - t0}")
            rate = window / (t1 - t0).total_seconds()
            logger.info(f"PERFORMANCE Rate is {rate} sims per second  div: {division}")
            t0 = t1

        # End of division loop

        # Score the results
        field_score = score_frame(cFrame, division, "Field")
        start_score = score_frame(cFrame, division, "Start")

        day_spread_score = check_consecutive(cFrame, division)

        total_score = field_score + start_score + day_spread_score

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

            # Revert to empty frame
            cFrame = backup_frame.copy()
            # cFrame = clear_division(division, cFrame)
        elif loop_count > max_loops:
            # We're done
            break

        else:
            # otherwise just increase seed
            random_seed += 1
            # Revert to empty frame
            cFrame = backup_frame.copy()
            # cFrame = clear_division(division, cFrame)

    # break


save_frame(cFrame, "calendar.pkl")
publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")
