# Season details

from datetime import timedelta, datetime

# Duplicate of helpers.py (circumvent circular import??)
def date_string_to_datetime(date):
    # print(f"Converting {date} to datetime")
    return datetime.strptime(date, "%m/%d/%Y")


start_date = date_string_to_datetime("3/2/2024")

week_split_data = {}
for week in range(1, 20):
    week_split_data[f"Week {week}"] = start_date + timedelta(7) * (week - 1)
    #print(f"Week {week} - {week_split_data[f'Week {week}']}")


blackout_dates = [
    "4/7/2024",  # Giants
    "3/30/2024",  # Easter Weekend
    "3/31/2024",  # Easter Weekend
    "5/25/2024",  # Memorial Day Weekend
    "5/26/2024",
    "5/27/2024",
]
# Datetime conversion for blackouts
blackout_days = [date_string_to_datetime(item) for item in blackout_dates]

division_info = {
    "Tee Ball": {
        "teams": 12,
        "weekend_pattern": [0, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 0],
        "preferred_days": ["Saturday"],
        "time_length": "90",
        "random_seed": 1737,
        "max_loops": 10,

    },
    "Lower Farm": {
        "teams": 12,
        "weekend_pattern": [6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0],
        "preferred_days": ["Sunday"],
        "time_length": "120",
        "random_seed": 1582,
        "max_loops": 10,
    },
    "Upper Farm": {
        "teams": 12,
        "weekend_pattern": [7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 0],
        "preferred_days": [
            ["Sunday"],
            ["Saturday"],
        ],
        "time_length": "120",
        "preferred_fields": [
            ["Ft. Scott - North", "Larsen", "Laurel Hill", "Ft. Scott - South", "Eureka"],
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
        "teams": 10,  # 1  2  3  4  TI E  7  8  9  10 11 12 13
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
        "games": 10,
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
        "teams": 10,
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
        "games": 10,
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
        "teams": 10,
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
        "teams": 10,
        "weekend_pattern": [5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 0, 0, 0],
        "weekday_pattern": [5, 4, 4, 4, 4, 5, 4, 4, 4, 0, 0, 0, 0],
        "time_length": "150",
        "random_seed": 292,  # 1.579 with seed 292
        "max_loops": 200,
        "denied_fields": ["Kimbell D3 SW", "Ft. Scott - South", "Rossi Park #1"],
    },
    "Juniors": {
        "teams": 6, "games": 9, "skip_weeks": ["11", "12", "13"], "time_length": "180", 
        "denied_fields": ["Riordan"],
        "playoffs": None,
    }
}

# https://sfrecpark.org/525/Individual-Field-Maps
field_info = {
    "Christopher": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Crocker Amazon D3": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "dirt",
    },
    "Crocker Amazon D4": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "dirt",
    },
    "Crocker Amazon D5": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "dirt",
    },
    "Eureka": {"Region": "SF", "Size": "46/60", "Type": "grass", "Infield":  "dirt"},
    "Fort Scott - North Diamond": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Fort Scott - South Diamond": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "dirt",
    },
    "Generic SFRPD Field": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "dirt",
    },
    "Holly Park": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "dirt",
    },
    "Ketcham - Field 1": {"Region": "TI", "Size": "46/60", "Type": "grass", "Infield":  "dirt"},
    "Kimbell - Diamond 1": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "turf",
        "Infield":  "turf",
    },
    "Kimbell - Diamond 2": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "turf",
        "Infield":  "turf",
    },
    "Kimbell - Diamond 3": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "turf",
        "Infield":  "turf",
    },
    "Lang D1": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "turf",
        "Infield":  "turf",
    },
    "Larsen - Field 1": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Laurel Hill - Field 1": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Louis Sutter  D1": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "dirt",
    },
    "Louis Sutter  D2": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "dirt",
    },
    "McCoppin": {
        "Region": "SF",
        "Size": "60/90",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Moscone D1": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Moscone D2": {
        "Region": "SF",
        "Size": "60/90",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Moscone D3": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Moscone D4": {
        "Region": "SF",
        "Size": "60/90",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Palega D2": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Paul Goode - Main": {
        "Region": "SF",
        "Size": "60/90",
        "Type": "turf",
        "Infield":  "turf",
    },
    "Paul Goode - Practice": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "turf",
        "Infield":  "turf",
    },
    "Potrero D2": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "dirt",
    },
    "Rossi - Field 1": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "grass",
    },
    "Rossi - Field 2": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "grass",
    },
    "South Sunset - Diamond 1": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "turf",
        "Infield":  "turf",
    },
    "South Sunset - Diamond 2": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "turf",
        "Infield":  "turf",
    },
    "Silver Terrace D1": {
        "Region": "SF",
        "Size": "60/90",
        "Type": "turf",
        "Infield":  "turf",
    },
    "Silver Terrace D2": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "turf",
        "Infield":  "turf",
    },
    "Sunset Rec": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "dirt",
    },
    "Balboa - Sweeney": {"Region": "SF", "Size": "60/90", "Type": "grass", "Infield":  "grass"},
    "Tepper - Field 1": {"Region": "TI", "Size": "46/60", "Type": "grass", "Infield":  "grass"},
    "Riordan": {"Region": "SF", "Size": "60/90", "Type": "turf", "Infield":  "turf"},
    "West Sunset - Field 3": {
        "Region": "SF",
        "Size": "46/60",
        "Type": "grass",
        "Infield":  "grass",
    },
    "West Sunset #1": {
        "Region": "SF",
        "Size": "60/90",
        "Type": "grass",
        "Infield":  "grass",
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
        ## HOWARD Email

        # “Team 1”: “Diamondbacks”,
        # “Team 2”: “Athletics”,
        # “Team 3”: “Red Sox”,
        # “Team 4”: “Giants”,
        # “Team 5”: “Cubs”,
        # “Team 6”: “Royals”,
        # “Team 7”: “Phillies”,
        # “Team 8”: “White Sox”,
        # “Team 9”: “Pirates”,
        # “Team 10”: “Angels”,
        "Team 1": "Diamondbacks",
        "Team 2": "Athletics",
        "Team 3": "Red Sox",
        "Team 4": "Giants",
        "Team 5": "Cubs",
        "Team 6": "Royals",
        "Team 7": "Phillies",
        "Team 8": "White Sox",
        "Team 9": "Pirates",
        "Team 10": "Angels",
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
    "Challenger": {
        "Challenger": "Challenger",
    }
}

