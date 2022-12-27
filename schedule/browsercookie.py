from flask import request


class BrowserCookie:

    MOCK_COOKIE: dict = {
        "credentials": None,
        "authcookie": None
    }

    @classmethod
    def get_mock_cookie(cls) -> dict:
        return cls.MOCK_COOKIE

    @classmethod
    def get_encrypted_cookies(cls) -> dict:
        # TODO: make this actually get from the cookies.
        return cls.MOCK_COOKIE

    @classmethod
    def set_auth_cookie(cls, cookie: str):
        cls.MOCK_COOKIE["authcookie"] = cookie

    @classmethod
    def set_credentials_cookie(cls, email: str, pwd: str):
        cls.MOCK_COOKIE["credentials"] = {
            "email": email,
            "password": pwd
        }

    @classmethod
    def clear_auth_cookie(cls):
        cls.MOCK_COOKIE["authcookie"] = ""
