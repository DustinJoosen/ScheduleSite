import requests
import json
from settings.settings import Settings
from schedule.browsercookie import BrowserCookie
from schedule.cookieencryption import substitution_decryption


class Client:

    def __init__(self):
        self.base_url: str = "https://windesheimapi.azurewebsites.net"

    def request_schedule(self) -> list | None:
        headers: dict = self.__get_headers()

        windesheimid: str = self.request_windesheimid()
        if windesheimid is None:
            return None

        # Somethimes the forbidden_note string is in the cookie. if this happens, stop.
        forbidden_note: str = "…"
        if forbidden_note in headers['cookie']:
            print("The forbidden note has been found. Code red")
            return None

        response: Response = requests.get(f"{self.base_url}/api/v2/Persons/{windesheimid}/Rooster", headers=headers)
        if response.status_code == 200:
            try:
                content: list = json.loads(response.content)
                return content
            except ValueError:
                print("Could not convert response to JSON. The most likely cause is an invalid cookie.")
                BrowserCookie.clear_auth_cookie()
                return None

        print(f"Response code {response.status_code}.")
        return None

    def request_windesheimid(self) -> str | None:
        headers: dict = self.__get_headers()

        response: Response = requests.get(f"{self.base_url}/api/v1/Authorize/Roles", headers=headers)
        if response.status_code == 200:
            try:
                data: dict = json.loads(response.content)
                return data['data']['windesheimId']
            except ValueError:
                print("Could not convert response to JSON. The most likely cause is an invalid cookie.")
                BrowserCookie.clear_auth_cookie()

        return None

    @staticmethod
    def __get_headers() -> dict:
        encrypted_auth_cookie: str = BrowserCookie.get_auth_cookie()
        if encrypted_auth_cookie is None:
            auth_cookie = ""
        else:
            auth_cookie: str = substitution_decryption(encrypted_auth_cookie)

        return {
            'content-type': 'application/json',
            'cookie': '.AspNet.Cookies=' + auth_cookie
        }
