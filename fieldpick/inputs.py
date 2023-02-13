# Season details

from datetime import timedelta, datetime

# Duplicate of helpers.py (circumvent circular import??)
def date_string_to_datetime(date):
    # print(f"Converting {date} to datetime")
    return datetime.strptime(date, "%m/%d/%Y")


start_date = date_string_to_datetime("3/4/2023")

week_split_data = {}
for week in range(1, 20):
    week_split_data[f"Week {week}"] = start_date + timedelta(7) * (week - 1)
# print(week_split_data)

blackout_dates = [
    "4/8/2023",  # Easter Weekend (+Giants)
    "4/9/2023",  # Easter Weekend
    "5/27/2023",  # Memorial Day Weekend
    "5/28/2023",
    "5/29/2023",
]
# Datetime conversion for blackouts
blackout_days = [date_string_to_datetime(item) for item in blackout_dates]

division_info = {
    "Tee Ball": {
        "teams": 14,  # 1  2  3  4  5  E  7  8  9  10 11 12 13
        "weekend_pattern": [0, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 0],
        "preferred_days": ["Saturday"],
        "time_length": "90",
        "preferred_fields": [["Larsen", "Paul Goode Practice"]],
        "random_seed": 1737,
        "max_loops": 10,

    },
    "Lower Farm": {
        "teams": 12,  # 1  2  3  4  5  E  7  8  9  10 11 12 13
        "weekend_pattern": [6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0],
        "preferred_days": ["Sunday"],
        "time_length": "120",
        "preferred_fields": [
            ["Larsen", "Paul Goode Practice"],
            ["Larsen", "Paul Goode Practice", "Ft. Scott - South", "Christopher"],
        ],
        "random_seed": 1582,
        "max_loops": 10,
    },
    "Upper Farm": {
        "teams": 14,  # 1  2  3  4  5  E  7  8  9  10 11 12 13
        "weekend_pattern": [7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 0],
        "preferred_days": [
            ["Sunday"],
            ["Saturday"],
        ],
        "time_length": "120",
        "preferred_fields": [
            [
                "Larsen",
                "Paul Goode Practice",
                "Ft. Scott - South",
                "Christopher",
                "Rossi Park #1",
            ],
        ],
        "random_seed": 1879,
        "max_loops": 10,
    },
    "Rookie": {
        "teams": 14,  # 1  2  3  4  TI E  7  8  9  10 11 12 13
        "weekend_pattern": [2, 6, 6, 6, 7, 0, 6, 6, 6, 0, 0, 0, 0],
        "weekday_pattern": [0, 0, 2, 1, 0, 0, 2, 1, 2, 0, 0, 0, 0],
        "preferred_days": [
            [
                "Saturday",
                "Sunday",
            ],
            ["Saturday", "Sunday", "Tuesday", "Wednesday", "Thursday"],
        ],
        "dedicated_ti_weekend": 5,
        "preferred_fields": [
            [
                "Rossi Park #1",
                "Ft. Scott - South",
                "Kimbell D3 SW",
                "South Sunset D1 North",
            ],
            ["Rossi Park #1", "South Sunset D2 South", "Ft. Scott - North", "Ft. Scott - South", "Kimbell D3 SW"],
            [None],
        ],
        "games": 11,
        "day_off": "Friday",
        "ti_weekday": 0,


        "time_length": "150",
        "random_seed": 3127,  # 1.729 with seed 1936
        "max_loops": 10,
    },
    "Minors AA": {
        "games": 12,
        "day_off": "Wednesday",
        "ti_weekday": 2,
        "preferred_fields": [
            [
                "Rossi Park #1",
                "Ft. Scott - North",
                "Kimbell D2 SE",
                "South Sunset D2 South",
            ],
            [None],
        ],
        "teams": 10,  # 1  2  3  4  5  E  7  8  9  10 11 12 13
        "weekend_pattern": [2, 5, 5, 5, 5, 0, 5, 5, 5, 0, 0, 0, 0],
        "weekday_pattern": [0, 1, 1, 2, 2, 4, 2, 1, 2, 0, 0, 0, 0],
        "dedicated_ti_weekend": 7,
        "time_length": "150",
        #"random_seed": 10511,

        "random_seed": 10511,
        "max_loops": 200,
        "denied_fields": ["Kimbell D3 SW"],
    },
    "Minors AAA": {
        "games": 12,
        "day_off": "Tuesday",
        "ti_weekday": 3,


        "preferred_fields": [
            [
                "Rossi Park #1",
                "Ft. Scott - North",
                "Kimbell D2 SE",
            ],
            [None],
        ],
        "preferred_days": [
            ["Saturday", "Sunday"],
            ["Wednesday", "Thursday", "Friday"],
            ["Saturday", "Sunday", "Tuesday"],
        ],
        "teams": 8,  # 1  2  3  4  5  E  7  8  9  10 11 12 13
        "weekend_pattern": [3, 4, 4, 4, 4, 0, 4, 4, 4, 0, 0, 0, 0],
        "weekday_pattern": [0, 0, 2, 2, 2, 4, 2, 2, 2, 0, 0, 0, 0],
        "dedicated_ti_weekend": 8,
        "time_length": "150",
        "random_seed": 1975,  # 1.040 with seed 567
        "max_loops": 200,
        "denied_fields": ["Kimbell D3 SW", "Ft. Scott - South"],
    },
    "Majors": {
        "games": 15,
        "day_off": "Thursday",
        "ti_weekday": 4,

        "preferred_fields": [
            [
                "Kimbell D1 NW",
                "Rossi Park #1",
                "Ft. Scott - North",
                "Kimbell D2 SE",
            ],
            [None],
        ],
        "preferred_days": [
            ["Saturday", "Sunday"],
            ["Tuesday", "Wednesday", "Friday"],
            ["Saturday", "Sunday", "Tuesday"],
        ],
        "teams": 10,  # 1  2  3  4  5  E  7  8  9  10 11 12 13
        "weekend_pattern": [5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 0, 0, 0],
        "weekday_pattern": [5, 4, 4, 4, 4, 5, 4, 4, 4, 0, 0, 0, 0],
        "time_length": "150",
        "random_seed": 292,  # 1.579 with seed 292
        "max_loops": 200,
        "denied_fields": ["Kimbell D3 SW", "Ft. Scott - South", "Rossi Park #1"],
    },
    "Juniors": {
        "teams": 7, "games": 9, "skip_weeks": ["11", "12", "13"], "time_length": "180", 
        "denied_fields": ["Riordan"],
        "playoffs": None,
    }
}

# https://sfrecpark.org/525/Individual-Field-Maps
field_info = {
    "Christopher": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "grass",
    },
    "Crocker Amazon D3": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "dirt",
    },
    "Crocker Amazon D4": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "dirt",
    },
    "Crocker Amazon D5": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "dirt",
    },
    "Eureka": {"location": "SF", "size": "46/60", "type": "grass", "infield": "dirt"},
    "Ft. Scott - North": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "grass",
    },
    "Ft. Scott - South": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "dirt",
    },
    "Generic SFRPD Field": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "dirt",
    },
    "Holly Park": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "dirt",
    },
    "Ketcham": {"location": "TI", "size": "46/60", "type": "grass", "infield": "dirt"},
    "Kimbell D1 NW": {
        "location": "SF",
        "size": "46/60",
        "type": "turf",
        "infield": "turf",
    },
    "Kimbell D2 SE": {
        "location": "SF",
        "size": "46/60",
        "type": "turf",
        "infield": "turf",
    },
    "Kimbell D3 SW": {
        "location": "SF",
        "size": "46/60",
        "type": "turf",
        "infield": "turf",
    },
    "Lang D1": {
        "location": "SF",
        "size": "46/60",
        "type": "turf",
        "infield": "turf",
    },
    "Larsen": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "grass",
    },
    "Louis Sutter  D1": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "dirt",
    },
    "Louis Sutter  D2": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "dirt",
    },
    "McCoppin": {
        "location": "SF",
        "size": "60/90",
        "type": "grass",
        "infield": "grass",
    },
    "Moscone D1": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "grass",
    },
    "Moscone D2": {
        "location": "SF",
        "size": "60/90",
        "type": "grass",
        "infield": "grass",
    },
    "Moscone D3": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "grass",
    },
    "Moscone D4": {
        "location": "SF",
        "size": "60/90",
        "type": "grass",
        "infield": "grass",
    },
    "Palega D2": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "grass",
    },
    "Paul Goode Main": {
        "location": "SF",
        "size": "60/90",
        "type": "turf",
        "infield": "turf",
    },
    "Paul Goode Practice": {
        "location": "SF",
        "size": "46/60",
        "type": "turf",
        "infield": "turf",
    },
    "Potrero D2": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "dirt",
    },
    "Rossi Park #1": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "grass",
    },
    "South Sunset D1 North": {
        "location": "SF",
        "size": "46/60",
        "type": "turf",
        "infield": "turf",
    },
    "South Sunset D2 South": {
        "location": "SF",
        "size": "46/60",
        "type": "turf",
        "infield": "turf",
    },
    "Silver Terrace D1": {
        "location": "SF",
        "size": "60/90",
        "type": "turf",
        "infield": "turf",
    },
    "Silver Terrace D2": {
        "location": "SF",
        "size": "46/60",
        "type": "turf",
        "infield": "turf",
    },
    "Sunset Rec": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "dirt",
    },
    "Balboa - Sweeney": {"location": "SF", "size": "60/90", "type": "grass", "infield": "grass"},
    "Tepper": {"location": "TI", "size": "46/60", "type": "grass", "infield": "grass"},
    "Riordan": {"location": "SF", "size": "60/90", "type": "turf", "infield": "turf"},
    "West Sunset #3": {
        "location": "SF",
        "size": "46/60",
        "type": "grass",
        "infield": "grass",
    },
    "West Sunset #1": {
        "location": "SF",
        "size": "60/90",
        "type": "grass",
        "infield": "grass",
    },
}


team_names = {
# Tee Ball Team 1	Rays
# Tee Ball Team 10	Angels
# Tee Ball Team 11	Rockies
# Tee Ball Team 12	Phillies
# Tee Ball Team 13	Pirates
# Tee Ball Team 14	Athletics
# Tee Ball Team 2	Giants
# Tee Ball Team 3	Royals
# Tee Ball Team 4	White Sox
# Tee Ball Team 5	Diamondbacks
# Tee Ball Team 6	Reds
# Tee Ball Team 7	Cubs
# Tee Ball Team 8	Guardians
# Tee Ball Team 9	Red Sox
    "Tee Ball": {
        "Team 1": "Rays",
        "Team 10": "Angels",
        "Team 11": "Rockies",
        "Team 12": "Phillies",
        "Team 13": "Pirates",
        "Team 14": "Athletics",
        "Team 2": "Giants",
        "Team 3": "Royals",
        "Team 4": "White Sox",
        "Team 5": "Diamondbacks",
        "Team 6": "Reds",
        "Team 7": "Cubs",
        "Team 8": "Guardians",
        "Team 9": "Red Sox",
    },

# Upper Farm Team 1	Reds
# Upper Farm Team 10	Rockies
# Upper Farm Team 11	White Sox
# Upper Farm Team 12	Angels
# Upper Farm Team 13	Diamondbacks
# Upper Farm Team 14	Pirates
# Upper Farm Team 2	Rays
# Upper Farm Team 3	Cubs
# Upper Farm Team 4	Athletics
# Upper Farm Team 5	Red Sox
# Upper Farm Team 6	Guardians
# Upper Farm Team 7	Giants
# Upper Farm Team 8	Phillies
# Upper Farm Team 9	Royals
    "Upper Farm": {
        "Team 1": "Reds",
        "Team 10": "Rockies",
        "Team 11": "White Sox",
        "Team 12": "Angels",
        "Team 13": "Diamondbacks",
        "Team 14": "Pirates",
        "Team 2": "Rays",
        "Team 3": "Cubs",
        "Team 4": "Athletics",
        "Team 5": "Red Sox",
        "Team 6": "Guardians",
        "Team 7": "Giants",
        "Team 8": "Phillies",
        "Team 9": "Royals",

    },

# Lower Farm Team 1	Rays
# Lower Farm Team 10	Cubs
# Lower Farm Team 11	Royals
# Lower Farm Team 12	Angels
# Lower Farm Team 2	Giants
# Lower Farm Team 3	White Sox
# Lower Farm Team 4	Phillies
# Lower Farm Team 5	Pirates
# Lower Farm Team 6	Red Sox
# Lower Farm Team 7	Athletics
# Lower Farm Team 8	Reds
# Lower Farm Team 9	Diamondbacks
    "Lower Farm": {
        "Team 1": "Rays",
        "Team 10": "Cubs",
        "Team 11": "Royals",
        "Team 12": "Angels",
        "Team 2": "Giants",
        "Team 3": "White Sox",
        "Team 4": "Phillies",
        "Team 5": "Pirates",
        "Team 6": "Red Sox",
        "Team 7": "Athletics",
        "Team 8": "Reds",
        "Team 9": "Diamondbacks",
    },
    "Rookie": {
        # Rookie Team 1	Cubs
        # Rookie Team 10	Angels
        # Rookie Team 11	White Sox
        # Rookie Team 12	Athletics
        # Rookie Team 13	Reds
        # Rookie Team 14	Rockies
        # Rookie Team 2	Phillies
        # Rookie Team 3	Guardians
        # Rookie Team 4	Diamondbacks
        # Rookie Team 5	Royals
        # Rookie Team 6	Pirates
        # Rookie Team 7	Rays
        # Rookie Team 8	Red Sox
        # Rookie Team 9	Giants
        "Team 1": "Cubs",
        "Team 10": "Angels",
        "Team 11": "White Sox",
        "Team 12": "Athletics",
        "Team 13": "Reds",
        "Team 14": "Rockies",
        "Team 2": "Phillies",
        "Team 3": "Guardians",
        "Team 4": "Diamondbacks",
        "Team 5": "Royals",
        "Team 6": "Pirates",
        "Team 7": "Rays",
        "Team 8": "Red Sox",
        "Team 9": "Giants",
        },
    "Minors AA": {
        # AA Minors Team 1	Red Sox
        # AA Minors Team 10	Diamondbacks
        # AA Minors Team 2	Pirates
        # AA Minors Team 3	Giants
        # AA Minors Team 4	Angles
        # AA Minors Team 5	Cubs
        # AA Minors Team 6	Phillies
        # AA Minors Team 7	Athletics
        # AA Minors Team 8	Royals
        # AA Minors Team 9	White Sox
        "Team 1": "Red Sox",
        "Team 10": "Diamondbacks",
        "Team 2": "Pirates",
        "Team 3": "Giants",
        "Team 4": "Angels",
        "Team 5": "Cubs",
        "Team 6": "Phillies",
        "Team 7": "Athletics",
        "Team 8": "Royals",
        "Team 9": "White Sox",
    },

    "Minors AAA": {
        # AAA Minors Team 1	White Sox
        # AAA Minors Team 2	Red Sox
        # AAA Minors Team 3	Phillies
        # AAA Minors Team 4	Cubs
        # AAA Minors Team 5	Giants
        # AAA Minors Team 6	Angels
        # AAA Minors Team 7	Diamondbacks
        # AAA Minors Team 8	Athletics
        "Team 1": "White Sox",
        "Team 2": "Red Sox",
        "Team 3": "Phillies",
        "Team 4": "Cubs",
        "Team 5": "Giants",
        "Team 6": "Angels",
        "Team 7": "Diamondbacks",
        "Team 8": "Athletics",
    },

    "Majors": {

        # Majors Team 1	Giants
        # Majors Team 10	Phillies
        # Majors Team 2	Athletics
        # Majors Team 3	Angels
        # Majors Team 4	Royals
        # Majors Team 5	Diamondbacks
        # Majors Team 6	Cubs
        # Majors Team 7	White Sox
        # Majors Team 8	Pirates
        # Majors Team 9	Red Sox
        # 
        # 
        "Team 1": "Giants",
        "Team 10": "Phillies",
        "Team 2": "Athletics",
        "Team 3": "Angels",
        "Team 4": "Royals",
        "Team 5": "Diamondbacks",
        "Team 6": "Cubs",
        "Team 7": "White Sox",
        "Team 8": "Pirates",
        "Team 9": "Red Sox",
        },

    "Juniors": {
        # Juniors Team 1	Angels
        # Juniors Team 2	Mets
        # Juniors Team 3	Giants
        # Juniors Team 4	Cubs
        # Juniors Team 5	Red Sox
        # Juniors Team 6	Athletics
        # Juniors Team 7	Phillies
        "Team 1": "Angels",
        "Team 2": "Mets",
        "Team 3": "Giants",
        "Team 4": "Cubs",
        "Team 5": "Red Sox",
        "Team 6": "Athletics",
        "Team 7": "Phillies",
    },
}

