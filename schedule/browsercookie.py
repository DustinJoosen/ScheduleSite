from flask import request
from datetime import datetime


class BrowserCookie:

    MOCK_COOKIE: dict = {
        "authcookie": None,
        "credentials": None,
        "viewingdate": None
    }

    @classmethod
    def get_mock_cookie(cls) -> dict:
        return cls.MOCK_COOKIE

    @classmethod
    def get_auth_cookie(cls) -> str | None:
        return cls.MOCK_COOKIE["authcookie"]

    @classmethod
    def get_credentials_cookie(cls) -> list | None:
        return cls.MOCK_COOKIE["credentials"]

    @classmethod
    def get_viewingdate_cookie(cls) -> datetime | None:
        return cls.MOCK_COOKIE["viewingdate"]

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
    def set_viewingdate_cookie(cls, viewingdate: datetime):
        cls.MOCK_COOKIE["viewingdate"] = viewingdate

    @classmethod
    def clear_auth_cookie(cls):
        cls.set_auth_cookie(None)
