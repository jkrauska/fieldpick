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
    # "Challenger": {
    #     "teams": 4,
    #     "games": 2,
    #     "games_per_week": 2,
    #     "playoffs": None,
    #     "preferred_days": ["Sunday"],
    #     "preferred_fields": [["Riordan"],["Tepper"],["McCoppin"]],
    # },
    "Tee Ball": {
        "teams": 14,
        "games": 7,
        "games_per_week": 7,
        "playoffs": None,
        "preferred_days": ["Saturday"],
        "time_length": "90",
        "preferred_fields": [["Larsen", "Paul Goode Practice"]],
        "skip_weeks": ["1", "6", "13"],
        "random_seed": 132,
        "max_loops": 1,
    },
    "Lower Farm": {
        "teams": 12,
        "games": 6,
        "games_per_week": 6,
        "playoffs": None,
        "preferred_days": ["Sunday"],
        "time_length": "120",
        "skip_weeks": ["6", "13"],
        "preferred_fields": [
            ["Larsen", "Paul Goode Practice"],
            ["Larsen", "Paul Goode Practice", "Ft. Scott - South", "Christopher"],
        ],
        "random_seed": 2745,
        "max_loops": 1,
    },
    "Upper Farm": {
        "teams": 14,
        "games": 7,
        "games_per_week": 7,
        "playoffs": None,
        "preferred_days": [
            ["Sunday"],
            ["Saturday"],
        ],
        "time_length": "120",
        "skip_weeks": ["6", "13"],
        "preferred_fields": [
            [
                "Larsen",
                "Paul Goode Practice",
                "Ft. Scott - South",
                "Christopher",
                "Rossi Park #1",
            ],
        ],
        "random_seed": 859,
        "max_loops": 1,
    },
    "Rookie": {
        "teams": 14,
        "games": 7,
        "games_per_week": 7,
        "preferred_days": [
            ["Saturday", "Sunday"],
            ["Saturday", "Sunday", "Tuesday"],
        ],
        "preferred_fields": [
            [
                "Rossi Park #1",
                "South Sunset D2 South",
                "Ft. Scott - North",
            ],
            [None],
        ],
        "skip_weeks": ["6", "13"],
        "playoffs": None,
        "time_length": "150",
        "random_seed": 1342,
        "max_loops": 5,
    },
    "Minors AA": {
        "teams": 10,
        "games": 11,
        "games_per_week": 5,
        "playoffs": None,
        "time_length": "150",
    },
    "Minors AAA": {"teams": 8, "games": 11, "games_per_week": 4, "time_length": "150", "playoffs": None},
    "Majors": {"teams": 10, "games": 14, "games_per_week": 5, "playoffs": None},
    "Juniors": {"teams": 8, "games": 14, "playoffs": None},
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
