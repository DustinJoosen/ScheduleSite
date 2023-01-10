import pymongo.database
from flask import request
from datetime import datetime
from pymongo import MongoClient


class Mongo:

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
    def get_browser_guid(cls):
        if (mongo_browser_guid := request.cookies.get("mongo_browser_guid")) is not None:
            return mongo_browser_guid
        else:
            print("mongo_browser_guid cookie is None. a new guid is generated.")
            return "7d516d57-846e-4d8f-a311-15f3866fbc83"

    @classmethod
    def get_document_by_browser_guid(cls, browser_guid: str) -> dict | None:
        if not cls.CONNECTED:
            print("not connected.")
            return None

        return cls.DB.user_info.find_one({"browser_guid": browser_guid})

    @classmethod
    def get_mock_cookie(cls) -> dict:
        browser_guid: str = cls.get_browser_guid()
        return cls.get_document_by_browser_guid(browser_guid)

    @classmethod
    def get_auth_cookie(cls) -> str | None:
        browser_guid: str = cls.get_browser_guid()
        document = cls.get_document_by_browser_guid(browser_guid)
        try:
            return document["auth_cookie"]
        except KeyError:
            return None

    @classmethod
    def get_credentials_cookie(cls) -> list | None:
        browser_guid: str = cls.get_browser_guid()
        document = cls.get_document_by_browser_guid(browser_guid)
        try:
            return document["credentials"]
        except KeyError:
            return None

    @classmethod
    def get_viewingdate_cookie(cls) -> datetime | None:
        browser_guid: str = cls.get_browser_guid()
        document = cls.get_document_by_browser_guid(browser_guid)
        try:
            return document["viewingdate"]
        except KeyError:
            return None

    @classmethod
    def set_auth_cookie(cls, auth_cookie: str):
        if not cls.CONNECTED:
            print("not connected.")
            return None

        browser_guid: str = cls.get_browser_guid()

        cls.DB.user_info.update_one(
            {"browser_guid": browser_guid},
            {"$set": {"auth_cookie": auth_cookie}},
            upsert=True)

    @classmethod
    def set_credentials_cookie(cls, email: str, pwd: str):
        if not cls.CONNECTED:
            print("not connected.")
            return None

        browser_guid: str = cls.get_browser_guid()

        cls.DB.user_info.update_one(
            {"browser_guid": browser_guid},
            {"$set": {"credentials": {
                "email": email,
                "password": pwd
            }}},
            upsert=True)

    @classmethod
    def set_viewingdate_cookie(cls, viewingdate: datetime):
        if not cls.CONNECTED:
            print("not connected.")
            return None

        browser_guid: str = cls.get_browser_guid()

        cls.DB.user_info.update_one(
            {"browser_guid": browser_guid},
            {"$set": {"viewingdate": viewingdate}},
            upsert=True)

    @classmethod
    def clear_auth_cookie(cls):
        cls.set_auth_cookie(None)
