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
