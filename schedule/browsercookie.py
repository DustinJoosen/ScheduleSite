import pymongo.database
from flask import request
from datetime import datetime
from pymongo import MongoClient


class BrowserCookie:

    # PLAN: kijken of pypupeteer dit aankan.

    MOCK_COOKIE: dict = {
        "authcookie": None,
        "credentials": None,
        "viewingdate": None
    }

    CONNECTED: bool = False

    MONGO_CONN: MongoClient = None
    DB: pymongo.database.Database = None

    @classmethod
    def connect(cls):
        mongo_conn_string: str = "mongodb+srv://admin:<password>@cluster0.v5wbx7n.mongodb.net/?retryWrites=true&w=majority"
        cls.MONGO_CONN = MongoClient(mongo_conn_string)
        cls.DB = cls.MONGO_CONN.schedule_site

        cls.CONNECTED = True
        print("connected.")

    @classmethod
    def get_document_by_browser_guid(cls, browser_guid: str) -> dict | None:
        if not cls.CONNECTED:
            print("not connected.")
            return None

        return cls.DB.user_info.find_one({"browser_guid": browser_guid})

    @classmethod
    def get_mock_cookie(cls, browser_guid: str = None) -> dict:
        return cls.get_document_by_browser_guid(browser_guid)

    @classmethod
    def get_auth_cookie(cls, browser_guid: str = None) -> str | None:
        document = cls.get_document_by_browser_guid(browser_guid)
        try:
            return document["authcookie"]
        except KeyError:
            return None

    @classmethod
    def get_credentials_cookie(cls, browser_guid: str = None) -> list | None:
        document = cls.get_document_by_browser_guid(browser_guid)
        try:
            return document["credentials"]
        except KeyError:
            return None

    @classmethod
    def get_viewingdate_cookie(cls, browser_guid: str = None) -> datetime | None:
        document = cls.get_document_by_browser_guid(browser_guid)
        try:
            return document["viewingdate"]
        except KeyError:
            return None

    @classmethod
    def set_auth_cookie(cls, auth_cookie: str, browser_guid: str = None):
        if not cls.CONNECTED:
            print("not connected.")
            return None

        cls.DB.user_info.update_one(
            {"browser_guid": browser_guid},
            {"$set": {"auth_cookie": auth_cookie}},
            upsert=True)

    @classmethod
    def set_credentials_cookie(cls, email: str, pwd: str, browser_guid: str = None):
        if not cls.CONNECTED:
            print("not connected.")
            return None

        cls.DB.user_info.update_one(
            {"browser_guid": browser_guid},
            {"$set": {"credentials": {
                "email": email,
                "password": pwd
            }}},
            upsert=True)

    @classmethod
    def set_viewingdate_cookie(cls, viewingdate: datetime, browser_guid: str = None):
        if not cls.CONNECTED:
            print("not connected.")
            return None

        cls.DB.user_info.update_one(
            {"browser_guid": browser_guid},
            {"$set": {"viewingdate": viewingdate}},
            upsert=True)

    @classmethod
    def clear_auth_cookie(cls, browser_guid: str = None):
        cls.set_auth_cookie(None, browser_guid)


BrowserCookie.connect()

BROWSER_GUID: str = "7d516d57-846e-4d8f-a311-15f3866fbc82"
print(BrowserCookie.get_document_by_browser_guid(BROWSER_GUID))
print(BrowserCookie.clear_auth_cookie(BROWSER_GUID))
print(BrowserCookie.get_document_by_browser_guid(BROWSER_GUID))
