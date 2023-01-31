import pandas as pd

import logging
from inputs import division_info
from frametools import list_teams_for_division, weeks_in_season, save_frame, score_frame, reserve_slots, check_consecutive
from faceoffs import faceoffs_repeated
from gsheets import publish_df_to_gsheet
from datetime import datetime
from helpers import tepper_ketcham, short_division_names


from random import shuffle, seed

import numpy as np


logging.basicConfig(
    format="%(asctime)s %(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger()


# @profile
def main():
    # Main loop

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

    # Iterate over each division
    game_id_counter = 1

    for division in division_info.keys():

        random_seed = division_info[division].get("random_seed", 0)
        max_loops = division_info[division].get("max_loops", 1)
        count_teams = division_info[division].get("teams", 0)

        loop_count = 0
        best_score = 999
        best_seed = 0
        t0 = datetime.now()
        clean_faceoffs = []
        unused_faceoffs = []

        while loop_count <= max_loops:
            teams = list_teams_for_division(division, tFrame)

            seed(random_seed)  # Set random seed for this division
            faceoffs = faceoffs_repeated(teams, games=200)  # Make sure we have enough faceoffs to work with

            backup_frame = cFrame.copy()  # Save a copy of the calendar in case we need to revert
            backup_game_id_counter = game_id_counter

            logger.debug(f"Faceoffs for {division:<15}: {faceoffs}")
            logger.info("#" * 80)
            logger.info("#" * 80)

            logger.info(f"Processing {division:<15} with {len(teams)} teams   Loop {loop_count})")

            # Per division preferences
            if "games_per_week_pattern" in division_info[division]:
                games_per_week_pattern = division_info[division].get("games_per_week_pattern")
            else:
                games_per_week_pattern = None
                weekly_games_to_schedule = division_info[division].get("games_per_week", 0)

            if weekly_games_to_schedule == 0:
                logger.warning(f"\tNo games to schedule for {division:<15}")
                loop_count += 1
                continue

            preferred_fields = division_info[division].get("preferred_fields", [None])
            preferred_days = division_info[division].get("preferred_days", [None])

            logger.info(f"\tPreferred days: {preferred_days}")
            logger.info(f"\tPreferred fields: {preferred_fields}")

            # Lookup division preferences
            midweek_start = division_info[division].get("midweek_start", None)
            time_length = division_info[division].get("time_length", None)
            denied_fields = division_info[division].get("denied_fields", [])  # Things like Kimbell D3 for bigger kids
            dedicated_ti_weekend = division_info[division].get("dedicated_ti_weekend", None)

            # Create a working frame for this division
            query = "Division != Division and Notes != Notes and Time_Length == @time_length and Field not in @denied_fields"
            working_frame = cFrame.query(query)

            # Start walking weeks (Sat/Sun/Mon...Fri)
            for week in weeks_in_season(cFrame):

                # Skip weeks we don't want to schedule intentionally
                if week in division_info[division].get("skip_weeks", []):
                    logger.info(f"\t⤵ Skipping Week {week}")
                    continue

                # Determine total slots available this week
                this_week_slots = working_frame.query("Week_Number == @week")
                count_this_week_slots = len(this_week_slots)

                # Convoluted logic to determine number of games to schedule this week
                if True:  # nested for "clarity"
                    # See if we're in a changing pattern schedule
                    if games_per_week_pattern:
                        games_to_schedule = games_per_week_pattern[int(week) - 1]
                    else:
                        games_to_schedule = weekly_games_to_schedule  # Fixed number (younger kids)

                    logger.info(
                        f"{division:<15} Processing -- Week {week} -- Games To Schedule:{games_to_schedule}  -- Total Available Slots:{count_this_week_slots}"
                    )
                    if count_this_week_slots < games_to_schedule:
                        logger.warning(
                            f"{division:<15} ⚠️  There are fewer slots available than games to schedule in Week {week} ({count_this_week_slots} < {games_to_schedule})"
                        )

                # Try only grabbing clean faceoffs (no repeats)
                clean_slice = int(count_teams / 2)  # number of pure faceoffs/games before repeating teams
                clean_faceoffs = faceoffs[:clean_slice]
                del faceoffs[:clean_slice]
                # shuffle(clean_faceoffs)

                # Try each preferred day combination
                for preferred_days_set in preferred_days:
                    if games_to_schedule == 0:
                        continue

                    # if isinstance(preferred_fields, str):
                    #     preferred_fields = [preferred_fields]

                    # Try each preferred field combination
                    for preferred_fields_set in preferred_fields:
                        if games_to_schedule == 0:
                            continue

                        # Build query
                        field_query = "Division != Division"  # division is empty (unused slot)
                        # Add constraints to query if we have them
                        if preferred_days_set and preferred_days_set != [None]:
                            field_query += " and Day_of_Week in @preferred_days_set"
                        if preferred_fields_set and preferred_fields_set != [None]:
                            field_query += " and Field in @preferred_fields_set"

                        # FIXME Block Midweek here before 3/14/23
                        if midweek_start and int(week) < int(midweek_start):
                            weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                            field_query += " and Day_of_Week not in @weekdays"

                        cs = this_week_slots.query(field_query)

                        # Block dedicated TI weekend
                        if dedicated_ti_weekend:
                            if int(week) == int(dedicated_ti_weekend):
                                logger.info(f"{division:<15} Dedicated TI Weekend: {dedicated_ti_weekend}")
                                cs = cs.query("Field in @tepper_ketcham")
                            else:
                                # Only prune if we need to (queries are expensive)
                                if preferred_fields_set:
                                    if (
                                        "Tepper" in preferred_fields_set
                                        or "Ketcham" in preferred_fields_set
                                        or preferred_fields_set == [None]
                                    ):
                                        cs = cs.query("Field not in @tepper_ketcham")

                        candidate_slot_ids = cs.index.tolist()

                        # Shuffle the candidate slots
                        shuffle(candidate_slot_ids)
                        logger.info(f"Found {len(candidate_slot_ids)} candidate slots: {candidate_slot_ids}")

                        # Try each candidate slot
                        while len(candidate_slot_ids) > 0:
                            slot = candidate_slot_ids.pop(0)

                            # Confirm home team is not already scheduled
                            if pd.isnull(cFrame.loc[slot, "Home_Team"]):
                                logger.debug(f"\t\tSlot {slot} is available")

                                # Grab a faceoff
                                if clean_faceoffs:
                                    (home_team, away_team) = clean_faceoffs.pop(0)
                                else:
                                    logger.info("No more faceoffs to process ..  trying unused faceoffs")
                                    try:
                                        shuffle(unused_faceoffs)
                                        (home_team, away_team) = unused_faceoffs.pop(0)
                                    except IndexError:
                                        # pull another set of clean
                                        clean_faceoffs = faceoffs[:clean_slice]
                                        del faceoffs[:clean_slice]
                                        # shuffle(clean_faceoffs)

                                # Assign the teams to the slot
                                game_id_string = f"{short_division_names[division]}-{game_id_counter:03d}"
                                game_id_counter += 1
                                cFrame.loc[slot, ["Division", "Home_Team", "Away_Team", "Game_ID"]] = [
                                    division,
                                    home_team,
                                    away_team,
                                    game_id_string,
                                ]

                                # Get full details on the slot
                                row = cFrame.loc[slot]

                                games_to_schedule -= 1

                                logger.info(
                                    f"{division:<15} Placed {home_team:<7} vs {away_team:<7} in slot {slot:>3} at {row.Field:<24} on {row.Day_of_Week:>8} {row.Datestamp} - Games Left:{games_to_schedule}"
                                )
                                if games_to_schedule == 0:
                                    logger.info(f"{division:<15} ✅ No more games to schedule")
                                    break

                            else:
                                logger.debug(f"\t\tSlot {slot} is unavailable")
                                continue

                if games_to_schedule > 0:
                    logger.warning(f"{division:<15} ❌ Unable to schedule {games_to_schedule} games in week {week}")

            # End of division loop

            # Score the results

            # init scores
            field_score = 0
            start_score = 0
            day_spread_score = 0

            day_spread_score = check_consecutive(cFrame, division)
            field_score = score_frame(cFrame, division, "Field")
            start_score = score_frame(cFrame, division, "Start")

            total_score = field_score + start_score + day_spread_score

            # Track best score
            if total_score < best_score:
                best_score = total_score
                best_seed = random_seed

            window = 100
            if loop_count % window == 0 and loop_count > 0:
                logger.info(f"Loop {loop_count} of {max_loops}")
                t1 = datetime.now()
                logger.info(f"Elapsed time: {t1 - t0}")
                rate = window / (t1 - t0).total_seconds()
                logger.warning(f"{division:<15} PERFORMANCE Rate is {rate:0.2f} sims per second")
                logger.info(
                    f"{division:<15} SCORES Best: {best_seed}:{best_score:0.2f}  Current: {random_seed}:{total_score:0.2f}  trying {max_loops - loop_count} loops"
                )

                t0 = t1

            loop_count += 1

            logger.info(f"Loop {loop_count} of {max_loops}")

            # Annoyed about this logic vs the while loop
            if max_loops == 1:
                # Not looping, so just exit
                logger.info(f"{division:<15} Best SCORE is {best_seed}:{best_score:0.2f}")
                break
            elif loop_count == max_loops:
                # intentionally set to best result for last run
                logger.warning(f"{division:<15} RERUNNING Best SCORE for is {best_score:0.2f} with seed {best_seed}")
                random_seed = best_seed

                # Revert to empty frame
                cFrame = backup_frame.copy()
                game_id_counter = backup_game_id_counter

            elif loop_count > max_loops:
                # We're done (FIXME this is gross)
                break

            else:
                # otherwise just increase seed
                random_seed += 1

                # Revert to empty frame
                cFrame = backup_frame.copy()
                game_id_counter = backup_game_id_counter

        # break

    save_frame(cFrame, "calendar.pkl")
    publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")


if __name__ == "__main__":
    # Run the main function
    main()

    # Save the frame
