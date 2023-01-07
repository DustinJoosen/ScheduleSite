from schedule.client import Client
from schedule.processing import filter_schedule, convert_dates, set_type, group_by_date
from flask_caching import Cache, current_app


def get_schedule(show_zelfstudie: bool = True, cache: Cache = None) -> dict:
    # Check if the raw schedule is already saved inside the cache. Might save a request, and a few seconds.
    with current_app.app_context():
        # If the cache has a raw_schedule, use that. If not, send a request and add it to the cache.
        if (raw_schedule := cache.get("raw_schedule")) is None:
            client: Client = Client()

            windesheimid: str = client.request_windesheimid()
            raw_schedule = client.request_schedule(windesheimid)

            if raw_schedule is None:
                return {'error': 'schedule_is_none'}

            print("yo. we just did an ENTIRE request for the schedule. this bitch is now saved in the cache ( ︶︿︶)_╭∩╮")
            cache.set("raw_schedule", raw_schedule)

    if raw_schedule is None:
        return {'error': 'schedule_is_none'}

    # Process the schedule. Filter it, convert it, type it, group it.
    filtered_schedule: list = filter_schedule(raw_schedule, show_zelfstudie)
    converted_schedule: list = convert_dates(filtered_schedule)
    typed_schedule: list = set_type(converted_schedule)
    grouped_schedule: dict = group_by_date(typed_schedule)

    return grouped_schedule

