import json
from datetime import datetime, timedelta
from schedule.browsercookie import Cookie
from schedule.cookieencryption import transposition_decryption, transposition_encryption, substitution_decryption
from schedule.cookiegeneration import CookieGenerator


class Settings:
    COOKIE: str = ""
    CLASS_NAME: str = "WFHBOICT22.VG"

    TODAY: datetime = None
    VIEWING_DATE: datetime = None
    F_DAY_OF_WEEK: datetime = None
    L_DAY_OF_WEEK: datetime = None

    @classmethod
    def load(cls):
        # with open("settings/settings.json", 'r') as handle:
        #     content = json.load(handle)
        #
        #     cls.COOKIE = content['COOKIE']
        #     cls.CLASS_NAME = content['CLASS_NAME']

        # Set the cookies.
        cookie_info: dict = Cookie.get_encrypted_cookies()

        # If the auth cookie is set, decrypt it and set it.
        if cookie_info["authcookie"] is not None:
            decrypted_cookie: str = transposition_decryption(cookie_info["authcookie"])
            cls.COOKIE = decrypted_cookie
        else:
            # Check if the credentials are set.
            if cookie_info["credentials"] is not None:

                # Decrypt the credentials
                decrypted_username = substitution_decryption(cookie_info["credentials"]["email"])
                decrypted_password = substitution_decryption(cookie_info["credentials"]["password"])

                # Generate the new cookie.
                cg: CookieGenerator = CookieGenerator(decrypted_username, decrypted_password)
                cg.init_acynchronous_method(cg.set_aspnet_cookie)

                # Set the cookie, encrypt it and add it to the browser cookies.
                cls.COOKIE = cg.cookie

                encrypted_cookie: str = transposition_encryption(cg.cookie)
                Cookie.set_cookie(encrypted_cookie)
            else:
                raise Exception("no credentials supplied")

        # This is because the api gives the roosterdatum like this.
        cls.VIEWING_DATE = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        cls.TODAY = cls.VIEWING_DATE

        cls.F_DAY_OF_WEEK: datetime = cls.VIEWING_DATE - timedelta(days=cls.VIEWING_DATE.weekday())
        cls.L_DAY_OF_WEEK: datetime = cls.F_DAY_OF_WEEK + timedelta(days=4)
