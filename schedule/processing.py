import datetime
from settings.settings import Settings


# Filter unneccesairy records out of the schedule
def filter_schedule(schedule: list, show_zelfstudie: bool) -> list:
    filtered: list = []

    f_day_str: str = datetime.datetime.strftime(Settings.F_DAY_OF_WEEK, "%Y-%m-%dT%H:%M:%SZ")
    l_day_str: str = datetime.datetime.strftime(Settings.L_DAY_OF_WEEK, "%Y-%m-%dT%H:%M:%SZ")

    for record in schedule:

        # If the date of the record is not within the specified range, ignore it.
        if not (f_day_str <= record["roosterdatum"] <= l_day_str):
            continue

        # If the string 'zelfstudie' is inside the publicatietekst, and zelfstudie has to be filtered out, ignore it.
        if (not show_zelfstudie) and "zelfstudie" in record["publicatietekst"].lower():
            continue

        # It wasn't caught in the filters, so add it to the filtered list.
        filtered.append(record)

    return filtered


# Convert all the times from UNIX and string to datetime
def convert_dates(schedule: list) -> list:
    for record in schedule:
        starttijd = float(str(record["starttijd"])[0:10])
        eindtijd = float(str(record["eindtijd"])[0:10])

        record["starttijd"] = datetime.datetime.utcfromtimestamp(starttijd)
        record["eindtijd"] = datetime.datetime.utcfromtimestamp(eindtijd)

        record["roosterdatum_datetime"] = datetime.datetime.strptime(record["roosterdatum"], "%Y-%m-%dT%H:%M:%SZ")

    return schedule


def set_type(schedule: list) -> list:

    for record in schedule:
        record["type"] = 'Werkcollege'
        if "zelfstudie" in record["publicatietekst"].lower():
            record["type"] = "Zelfstudie"

        if "hoorcollege" in record["commentaar"].lower():
            record["type"] = "Hoorcollege"

    return schedule


# Group all the record by date in a dictionary.
def group_by_date(schedule: list) -> dict:
    grouped: dict = {}

    for record in schedule:
        # Create a group if it doesn't exist.
        if not record["roosterdatum"] in grouped:
            grouped[record["roosterdatum"]] = []

        # Add the record to the group.
        grouped[record["roosterdatum"]].append(record)

    return grouped
