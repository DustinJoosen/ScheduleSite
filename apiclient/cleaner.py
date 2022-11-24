import datetime


# convert the timestamps
def clean(schedule: list) -> list:
    for record in schedule:
        begintijd = float(str(record["starttijd"])[0:10])
        eindtijd = float(str(record["eindtijd"])[0:10])

        record["starttijd"] = datetime.datetime.utcfromtimestamp(begintijd)
        record["eindtijd"] = datetime.datetime.utcfromtimestamp(eindtijd)

        record["roosterdatum_datetime"] = datetime.datetime.strptime(record["roosterdatum"], "%Y-%m-%dT%H:%M:%SZ")

    return schedule
