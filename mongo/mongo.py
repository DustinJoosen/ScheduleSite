import pymongo.database
from flask import request
from datetime import datetime
from pymongo import MongoClient
import uuid


class Mongo:

    QUEUE_UUID: list = []

    CONNECTED: bool = False

    MONGO_CONN: MongoClient = None
    DB: pymongo.database.Database = None

    @classmethod
    def connect(cls):
        print("connecting to mongodb.")
        mongo_conn_string: str = "mongodb+srv://admin:<password>>@cluster0.v5wbx7n.mongodb.net/?retryWrites=true&w=majority"
        cls.MONGO_CONN = MongoClient(mongo_conn_string)
        cls.DB = cls.MONGO_CONN.schedule_site

        cls.CONNECTED = True
        print("mongodb connection established.")

    @classmethod
    def get_browser_guid(cls):
        if (mongo_browser_guid := request.cookies.get("mongo_browser_guid")) is not None:
            return mongo_browser_guid
        return None

    @classmethod
    def insert_browser_guid_document(cls):
        if not cls.CONNECTED:
            print("not connected.")
            return None

        browser_guid: str = str(uuid.uuid1())

        cls.DB.user_info.insert_one({
            "browser_guid": browser_guid,
            "credentials": {
                "email": None,
                "password": None
            },
            "auth_cookie": None,
            "viewingdate": None
        })

        return browser_guid

    @classmethod
    def get_document_by_browser_guid(cls, browser_guid: str) -> dict | None:
        if not cls.CONNECTED:
            print("not connected.")
            return None

        return cls.DB.user_info.find_one({"browser_guid": browser_guid})

    @classmethod
    def get_mock_document(cls) -> dict:
        browser_guid: str = cls.get_browser_guid()
        return cls.get_document_by_browser_guid(browser_guid)

    @classmethod
    def get_auth_document(cls) -> str | None:
        browser_guid: str = cls.get_browser_guid()
        document = cls.get_document_by_browser_guid(browser_guid)
        try:
            return document["auth_cookie"]
        except KeyError:
            return None

    @classmethod
    def get_credentials_document(cls) -> list | None:
        browser_guid: str = cls.get_browser_guid()
        document = cls.get_document_by_browser_guid(browser_guid)
        try:
            return document["credentials"]
        except KeyError:
            return None

    @classmethod
    def get_viewingdate_document(cls) -> datetime | None:
        browser_guid: str = cls.get_browser_guid()
        document = cls.get_document_by_browser_guid(browser_guid)
        try:
            return document["viewingdate"]
        except KeyError:
            return None

    @classmethod
    def set_auth_document(cls, auth_cookie: str):
        if not cls.CONNECTED:
            print("not connected.")
            return None

        browser_guid: str = cls.get_browser_guid()

        cls.DB.user_info.update_one(
            {"browser_guid": browser_guid},
            {"$set": {"auth_cookie": auth_cookie}},
            upsert=True)

    @classmethod
    def set_credentials_document(cls, email: str, pwd: str):
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
    def set_viewingdate_document(cls, viewingdate: datetime):
        if not cls.CONNECTED:
            print("not connected.")
            return None

        browser_guid: str = cls.get_browser_guid()

        cls.DB.user_info.update_one(
            {"browser_guid": browser_guid},
            {"$set": {"viewingdate": viewingdate}},
            upsert=True)

    @classmethod
    def clear_auth_document(cls):
        cls.set_auth_document(None)
