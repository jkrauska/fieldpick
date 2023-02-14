# fieldpick

field pick league scheduling software used for San Francisco Little League

This code is the 4th version of the league scheduling software. 

It uses Pandas dataframes to store the calendar and team data and the pulp library to define and solve the schedule as a Linear Programming problem.




# Developer setup

1. Create a fresh python environment (ideally starting with a local python 3.10
```bash
python3 -m venv .venv
```

 2. Activate the environment and install requirements

```bash
source .venv/bin/activate
pip install -r requirements.txt
```
# User docs



## Preppping

run 
`python fieldpick/create-teams.py` 
to create the season team lists

run 
`python fieldpick/create-calendar.py` 
to create the season calendar/timeslots


New pulp approach is done per field time size.

see pulp150 and pulp180 for notes.


# Season Notes and Goals

**Warning** 
These are guidelines and not to be considered official policy of Little League.


## Lower Divisions

### Tee Ball
- Saturdays
- Smaller fields (eg. Paul Goode, Larsen)
- 90 minute time slots

### Lower Farm
- Sundays
- Smaller fields (eg. Paul Goode, Larsen, Christopher)
- 120 minute time slots

###  Upper Farm
- Saturdays
- Medium Fields (Christopher, Rossi, Fort Scott South)
- 120 minutes time slots


## Upper Divisions
- Adds midweek games
- No Mondays (as long as Rec/Park doesn't assign)
- Try to have one blocked of day for each Division
- 150 minute time slots
- With each step up, generally more games on TI fields

### Rookie
- No Mondays, No Fridays
- No TI Weekday
- Ft. Scott - South	Ft. Scott - North	Tepper	Ketcham	Kimbell D1 NW
- At least one game on TI

### Minors AA
- No Mondays, No Wednesdays
- Every weekend and every one week day every other week
- Every weekend and every one week day every other week
- At least one game on TI


### Minors AAA
- No Mondays, No Tuesdays
- Every weekend and every one week day every other week

### Majors
- More TI Weekdays (predominantly on TI in general)
- No Mondays, No Thursdays
- Before and after Challenger on Tepper on Sundays
- Shoot for every weekend and one day during the week

## Special Divisions

### Juniors
- Bigger fields (60/90) (Balboa - Sweeney, Paul Goode Main)
- 180 minute slots
- No TI
- Often PA will handle this schedule, but fields are set by time and size
- Spring 2023
-- 7 team (odd #, which is trickier to accommodate)
-- Had to allow back to back (one team per weekend sat/sun) to get 10 games per team


### Challenger
- Dedicated Tepper 2pm Sundays
- Put Majors on Tepper before and after them to assist
- Usually also gets a spot on Riordan.


### Softball
Not currently scheduled (2023)


## Field and Timing Notes


### Fields 

See inputs.py for specs like field size and turf vs grass, etc.

Balance Tepper and Ketcham on TI per team. 

Fields without fences are more appropriate for younger divisions.

Fields where the outfields are often used by other sports or casual use (eg. Rossi) are more appropriate for younger divisions.

Normally we "pre-carve" up these fields for lower divisions in to shorter time slots appropriate for the division.

### Timing

No Back to back games. (two days in a row) (exception for Juniors)

No more than 3 games in 5 consecutive days.

IDEAL: No more than 3 games in 6 consecutive days.

Be mindful of sunset times. (is looked up in schedule creation tool)

Some fields (Kimbell/South Sunset) have lights.

TI fields can go until 7pm (19:00) on weekends after the time change.
(4 games/day)
09:00-11:30
11:30-14:00
14:00-16:30
16:30-19:00

Typically we don't play on Easter weekend.

Typically we schedule a day at a Giants game. (Saturday before Easter in 2023)

Typically we don't play on Memorial Day weekend.


### Field Start vs Game Start

Field start is when we officially have access to the field.
Game start is when the first pitch should be thrown.

Field time is when the prior team should be off and new teams should take the fields for warmups. (Usually one team infield, one outfield and then swapped.)

For TB to Farm (90 and 120 min time slots), we start the game 15m after Field Start.

For Rookie and up (150 min time slots), we start the game 30m after Field Start.
