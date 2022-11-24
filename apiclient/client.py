import requests
import json
from apiclient.settings import Settings
from apiclient.filter import Filter
from apiclient.cleaner import clean


class Client:

    def __init__(self, min_date: str, max_date: str, show_zelfstudie: bool=True):
        self.base_url: str = "https://windesheimapi.azurewebsites.net/api/v2"
        self.filter: Filter = Filter(min_date, max_date, show_zelfstudie)

    def request_schedule(self) -> dict | None:
        headers: dict = {
            'content-type': 'application/json',
            'cookie': '.AspNet.Cookies=' + Settings.COOKIE
        }

        # Somethimes the forbidden_note string is in the cookie. if this happens, stop.
        forbidden_note: str = "…"
        if forbidden_note in headers['cookie']:
            print("The forbidden note has been found. Code red")
            return None

        response: Response = requests.get(f"{self.base_url}/klas/{Settings.CLASS_NAME}/les", headers=headers)
        if response.status_code == 200:

            # Temp. TODO: restructure this shit.
            content: list = []

            try:
                content: list = json.loads(response.content)
            except ValueError:
                print("Cookie is invalid. Cookie monster would be ashamed")
                return None
            finally:
                # Process the content
                filtered: list = self.filter.filter(content)
                cleaned: list = clean(filtered)
                grouped: dict = self.group_by_date(cleaned)

                return grouped

        print(f"Response code {response.status_code}.")
        return None

    def group_by_date(self, schedule: list) -> dict:
        grouped_schedule: dict = {}
        for record in schedule:
            if not record["roosterdatum"] in grouped_schedule:
                grouped_schedule[record["roosterdatum"]] = []

            grouped_schedule[record["roosterdatum"]].append(record)

        return grouped_schedule
