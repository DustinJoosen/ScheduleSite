import json
from datetime import datetime, timedelta


class Settings:
    COOKIE: str = ""
    CLASS_NAME: str = ""

    TODAY: datetime = None
    F_DAY_OF_WEEK: datetime = None
    L_DAY_OF_WEEK: datetime = None

    @classmethod
    def load(cls):
        with open("settings/settings.json", 'r') as handle:
            content = json.load(handle)

            cls.COOKIE = content['COOKIE']
            cls.CLASS_NAME = content['CLASS_NAME']

        # This is because the api gives the roosterdatum like this.
        cls.TODAY = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        cls.F_DAY_OF_WEEK: datetime = cls.TODAY - timedelta(days=cls.TODAY.weekday())
        cls.L_DAY_OF_WEEK: datetime = cls.F_DAY_OF_WEEK + timedelta(days=4)
