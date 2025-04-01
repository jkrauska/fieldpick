import pandas as pd

import logging
from inputs import division_info
from frametools import (
    list_teams_for_division,
    weeks_in_season,
    save_frame,
    score_frame,
    reserve_slots,
    check_consecutive,
    score_gamecount,
)
from faceoffs import faceoffs_repeated
from gsheets import publish_df_to_gsheet
from datetime import datetime
from helpers import tepper_ketcham, short_division_names

from collections import defaultdict


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
    cFrame.update(
        reserve_slots(
            cFrame,
            day_of_week="Sunday",
            field="Riordan",
            start="13:30",
            division="Challenger"))
    cFrame.update(
        reserve_slots(
            cFrame,
            day_of_week="Sunday",
            field="Tepper",
            start="14:00",
            division="Challenger"))
    cFrame.update(
        reserve_slots(
            cFrame,
            day_of_week="Sunday",
            field="McCoppin",
            start="09:00",
            division="Challenger",
            date="2025-03-09"))

    # Iterate over each division
    game_id_counter = 1

    # Iterate divisions
    for division in division_info.keys():
        division_config = division_info[division]

        random_seed = division_config.get("random_seed", 0)
        max_loops = division_config.get("max_loops", 1)
        count_teams = division_config.get("teams", 0)

        loop_count = 0
        best_score = 999
        best_seed = 0
        t0 = datetime.now()
        clean_faceoffs = []
        unused_faceoffs = []
        unable_score = 0

        phases = defaultdict(dict)

        if "weekend_pattern" in division_config:
            phases["weekend"] = division_config.get("weekend_pattern")
        if "weekday_pattern" in division_config:
            phases["weekday"] = division_config.get("weekday_pattern")

        # Lookup division preferences
        time_length = division_config.get("time_length", None)
        # Things like Kimbell D3 for bigger kids
        denied_fields = division_config.get("denied_fields", [])
        dedicated_ti_weekend = division_config.get(
            "dedicated_ti_weekend", None)

        teams = list_teams_for_division(division, tFrame)

        # Random chance looper
        while loop_count <= max_loops:
            # Make sure we have enough faceoffs to work with
            faceoffs = faceoffs_repeated(teams, games=200)

            seed(random_seed)  # Set random seed for this division

            # Make backups of the calendar and game_id_counter at start in case
            # we need to revert
            backup_frame = cFrame.copy()
            backup_game_id_counter = game_id_counter

            logger.info("#" * 80)
            logger.info(
                f"# Processing {
                    division:<15} with {
                    len(teams)} teams   Loop {loop_count})")

            preferred_fields = division_config.get("preferred_fields", [None])
            preferred_days = division_config.get("preferred_days", [None])

            logger.info(f"\tPreferred days: {preferred_days}")
            logger.info(f"\tPreferred fields: {preferred_fields}")

            # Create a working frame for this division
            query = "Division != Division and Notes != Notes and Time_Length == @time_length and Field not in @denied_fields"
            working_frame = cFrame.query(query)

            # Start walking weeks (Sat/Sun ... Mon...Fri)
            for week in weeks_in_season(cFrame):

                # First do weekend games, then do weekeday games
                for phase in phases.keys():

                    logger.info(f"## Processing Phase: {phase}")
                    games_per_week_pattern = phases[phase]

                    # Determine total slots available this week
                    this_week_slots = working_frame.query(
                        "Week_Number == @week")
                    count_this_week_slots = len(this_week_slots)

                    games_to_schedule = games_per_week_pattern[int(week) - 1]

                    logger.info(
                        f"{division:<15} Processing -- Week {week} -- Phase: {phase} -- Games To Schedule:{games_to_schedule}  -- Total Available Slots:{count_this_week_slots}  -- Total Faceoffs:{len(faceoffs)}"
                    )
                    if count_this_week_slots < games_to_schedule:
                        logger.warning(
                            f"{division:<15} ⚠️  There are fewer slots available than games to schedule in Week {week} ({count_this_week_slots} < {games_to_schedule})"
                        )

                    if games_to_schedule == 0:
                        logger.info(
                            f"{division:<15} No games to schedule in Phase {phase} Week {week}")
                        continue

                    # Try only grabbing clean faceoffs (no repeats)
                    # number of pure faceoffs/games before repeating teams
                    clean_slice = int(count_teams / 2)
                    clean_faceoffs = faceoffs[:clean_slice]
                    del faceoffs[:clean_slice]
                    shuffle(clean_faceoffs)

                    # Try each preferred day combination
                    for preferred_days_set in preferred_days:
                        if games_to_schedule == 0:
                            continue

                        # Try each preferred field combination
                        for preferred_fields_set in preferred_fields:
                            if games_to_schedule == 0:
                                continue

                            # Build query
                            # division is empty (unused slot)
                            field_query = "Division != Division"
                            # Add constraints to query if we have them
                            if preferred_days_set and preferred_days_set != [
                                    None]:
                                field_query += " and Day_of_Week in @preferred_days_set"
                            if preferred_fields_set and preferred_fields_set != [
                                    None]:
                                field_query += " and Field in @preferred_fields_set"

                            # Limit to weekends or weekdays
                            if phase == "weekend":
                                weekdays = [
                                    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                                field_query += " and Day_of_Week not in @weekdays"
                            elif phase == "weekday":
                                weekends = ["Saturday", "Sunday"]
                                field_query += " and Day_of_Week not in @weekends"

                            cs = this_week_slots.query(field_query)

                            # Block dedicated TI weekend
                            if dedicated_ti_weekend:
                                if int(week) == int(
                                        dedicated_ti_weekend) and phase == "weekend":
                                    logger.info(
                                        f"{division:<15} Dedicated TI Weekend: {dedicated_ti_weekend}")
                                    cs = cs.query("Field in @tepper_ketcham")
                                # else:
                                #     # Only prune if we need to (queries are expensive)
                                #     if preferred_fields_set:
                                #         if (
                                #             "Tepper" in preferred_fields_set
                                #             or "Ketcham" in preferred_fields_set
                                #             or preferred_fields_set == [None]
                                #         ):
                                #             cs = cs.query("Field not in @tepper_ketcham")

                            candidate_slot_ids = cs.index.tolist()

                            # Shuffle the candidate slots
                            shuffle(candidate_slot_ids)
                            logger.info(
                                f"Found {
                                    len(candidate_slot_ids)} candidate slots: {candidate_slot_ids}")

                            # Try each candidate slot
                            while len(candidate_slot_ids) > 0:
                                slot = candidate_slot_ids.pop(0)
                                # Get full details on the slot
                                row = cFrame.loc[slot]

                                # Confirm home team is not already scheduled
                                if pd.isnull(cFrame.loc[slot, "Home_Team"]):
                                    logger.debug(
                                        f"\t\tSlot {slot} is available")

                                    # Grab a faceoff
                                    if clean_faceoffs:
                                        (home_team, away_team) = clean_faceoffs.pop(0)
                                        faceoff_source = "clean"
                                    else:
                                        logger.info(
                                            "No more faceoffs to process ..  trying unused faceoffs")
                                        if unused_faceoffs:
                                            shuffle(unused_faceoffs)
                                            (home_team,
                                             away_team) = unused_faceoffs.pop(0)
                                            faceoff_source = "unused"
                                        else:
                                            # pull another set of clean
                                            clean_faceoffs = faceoffs[:clean_slice]
                                            del faceoffs[:clean_slice]
                                            shuffle(clean_faceoffs)
                                            (home_team,
                                             away_team) = clean_faceoffs.pop(0)
                                            faceoff_source = "clean"
                                            # shuffle(clean_faceoffs)

                                    # FIXME: This might be a better place to check for back to backs. (don't even allow it to schedule.. move on, and block if you can't get enough..)
                                    # IT IS ALL SUPER SLOW
                                    # Doesn't seem to be catching any??
                                    # if division in ["Rookie", "Minors AAA", "Minors AA", "Majors"]:
                                    #     slot_day = int(row.Day_of_Year)
                                    #     slot_day_before = cFrame.query("Day_of_Year == @slot_day - 1 and Division == @division")
                                    #     slot_day_after = cFrame.query("Day_of_Year == @slot_day + 1 and Division == @division")

                                    #     check_home_before = slot_day_before.query("Home_Team == @home_team or Away_Team == @home_team")
                                    #     check_away_before = slot_day_before.query("Home_Team == @away_team or Away_Team == @away_team")

                                    #     check_home_after = slot_day_after.query("Home_Team == @home_team or Away_Team == @home_team")
                                    #     check_away_after = slot_day_after.query("Home_Team == @away_team or Away_Team == @away_team")

                                    #     if len(check_home_before) > 0 or len(check_home_after) > 0 or len(check_away_before) > 0 or len(check_away_after) > 0:
                                    #         logger.warning(f"⚠️  {division:<15} {home_team} would a back to back game in week {week} - skipping")
                                    #         logger.warning(f"back to back DEBUG HB{len(check_home_before)} HA{len(check_home_after)} AB{len(check_away_before)}  AA{len(check_away_after)}")

                                    #         # put team back
                                    #         if faceoff_source == "clean":
                                    #             clean_faceoffs.append((home_team, away_team))
                                    #         elif faceoff_source == "unused":
                                    #             unused_faceoffs.append((home_team, away_team))
                                    #         continue

                                    # Assign the teams to the slot
                                    game_id_string = f"{
                                        short_division_names[division]}-{
                                        game_id_counter:03d}"
                                    game_id_counter += 1
                                    cFrame.loc[slot,
                                               ["Division",
                                                "Home_Team",
                                                "Home_Team_Name",
                                                "Away_Team",
                                                "Away_Team_Name",
                                                "Game_ID"]] = [division,
                                                               home_team,
                                                               home_team,
                                                               away_team,
                                                               away_team,
                                                               game_id_string,
                                                               ]

                                    games_to_schedule -= 1

                                    logger.info(
                                        f"{
                                            division:<15} Placed {
                                            home_team:<7} vs {
                                            away_team:<7} in slot {
                                            slot:>3} at {
                                            row.Field:<24} on {
                                            row.Day_of_Week:>8} {
                                            row.Datestamp} - Games Left:{games_to_schedule}")
                                    if games_to_schedule == 0:
                                        logger.info(
                                            f"{division:<15} ✅ No more games to schedule")
                                        break

                                else:
                                    logger.debug(
                                        f"\t\tSlot {slot} is unavailable")
                                    continue

                    if games_to_schedule > 0:
                        logger.warning(
                            f"{division:<15} ❌ Unable to schedule {games_to_schedule} games in phase {phase} in week {week}"
                        )
                        unable_score += games_to_schedule

            # End of division loop

            # Score the results

            # init scores
            field_score = 0
            start_score = 0
            day_spread_score = 0
            gamecount_score = 0

            day_spread_score = check_consecutive(cFrame, division)
            field_score = score_frame(cFrame, division, "Field")
            start_score = score_frame(cFrame, division, "Start")

            gamecount_score = score_gamecount(cFrame, division)

            total_score = field_score + start_score + \
                day_spread_score + gamecount_score + unable_score
            logger.info(
                f"DEBUG SCORE {division} FS{
                    field_score:0.2f} SS{
                    start_score:0.2f} DS{
                    day_spread_score:0.2f} GC{
                    gamecount_score:0.2f} UA{
                        unable_score:0.2f}  {total_score}")

            # Track best score
            if total_score < best_score:
                best_score = total_score
                best_seed = random_seed

            # logger.info(f"{division:<15}  Current:{random_seed}:{total_score:0.2f}  SCORES Best: {best_seed}:{best_score:0.2f}")

            window = 50
            if loop_count % window == 0 and loop_count > 0:
                logger.info(f"Loop {loop_count} of {max_loops}")
                t1 = datetime.now()
                logger.info(f"Elapsed time: {t1 - t0}")
                rate = window / (t1 - t0).total_seconds()
                logger.warning(
                    f"{division:<15} PERFORMANCE Rate is {rate:0.2f} sims per second")
                logger.info(
                    f"{
                        division:<15} SCORES Best: {best_seed}:{
                        best_score:0.2f}  Current: {random_seed}:{
                        total_score:0.2f}  trying {
                        max_loops -
                        loop_count} loops")

                t0 = t1

            loop_count += 1

            logger.info(f"Loop {loop_count} of {max_loops}")

            # Annoyed about this logic vs the while loop
            if max_loops == 1:
                # Not looping, so just exit
                logger.info(
                    f"{division:<15} Best SCORE is {best_seed}:{best_score:0.2f}")
                break
            elif loop_count == max_loops:
                # intentionally set to best result for last run
                logger.warning(
                    f"{division:<15} Final Best SCORE is {best_seed}:{best_score:0.2f} - breaking early")

                logger.warning(
                    f"{division:<15} RERUNNING Best SCORE for is {best_score:0.2f} with seed {best_seed}")
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

            # Last catch.. If you think the score is really good enough, go
            # ahead and finish early
            if best_score < 1.1:
                logger.warning(
                    f"{division:<15} Final Best SCORE is {best_seed}:{best_score:0.2f} - breaking early")
                loop_count = max_loops
                random_seed = best_seed

                # Revert to empty frame
                cFrame = backup_frame.copy()
                game_id_counter = backup_game_id_counter

        save_frame(cFrame, f"calendar-{division}.pkl")
        # break

    save_frame(cFrame, "calendar.pkl")
    publish_df_to_gsheet(cFrame, worksheet_name="Full Schedule")


if __name__ == "__main__":
    # Run the main function
    main()

    # Save the frame
