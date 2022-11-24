# unites all classes.
from schedule.client import Client
from schedule.processing import filter_schedule, convert_dates, group_by_date


def get_schedule(show_zelfstudie: bool = True) -> dict:
    client: Client = Client()
    raw_schedule: list = client.request_schedule()

    filtered_schedule: list = filter_schedule(raw_schedule, show_zelfstudie)
    converted_schedule: list = convert_dates(filtered_schedule)
    grouped_schedule: dict = group_by_date(converted_schedule)

    return grouped_schedule

