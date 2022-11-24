import json


class Settings:
    COOKIE = ""
    CLASS_NAME = ""

    @classmethod
    def load(cls):
        with open("settings/settings.json", 'r') as handle:
            content = json.load(handle)

            cls.COOKIE = content['COOKIE']
            cls.CLASS_NAME = content['CLASS_NAME']
