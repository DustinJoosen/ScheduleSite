import requests
import json
from settings.settings import Settings


class Client:

    def __init__(self):
        self.base_url: str = "https://windesheimapi.azurewebsites.net/api/v2"

    def request_schedule(self) -> list | None:
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
            try:
                content: list = json.loads(response.content)
                return content
            except ValueError:
                print("Could not convert response to JSON. The most likely cause is an invalid cookie.")
                return None

        print(f"Response code {response.status_code}.")
        return None
