import json
from datetime import datetime, timedelta
from schedule.browsercookie import BrowserCookie
from schedule.cookieencryption import substitution_decryption, substitution_encryption
from schedule.cookiegeneration import CookieGenerator


class Settings:
    TODAY: datetime = None
    LOADED: bool = False

    @classmethod
    def load(cls):

        # Set the cookies.
        encrypted_auth_cookie: str = BrowserCookie.get_auth_cookie()

        # If the auth cookie is not yet set.
        if encrypted_auth_cookie is None:
            # Check if credentials are set.
            encrypted_credentials = BrowserCookie.get_credentials_cookie()
            if encrypted_credentials is None:
                raise Exception("no credentials supplied")

            # Decrypt the credentials
            decrypted_username = substitution_decryption(encrypted_credentials["email"])
            decrypted_password = substitution_decryption(encrypted_credentials["password"])

            # Generate the new cookie.
            cg: CookieGenerator = CookieGenerator(decrypted_username, decrypted_password)
            cg.init_acynchronous_method(cg.set_aspnet_cookie)

            # Encrypt the new cookie and set it to the browser cookies.
            encrypted_cookie: str = substitution_encryption(cg.cookie)
            BrowserCookie.set_auth_cookie(encrypted_cookie)

        # The API gives the time at 0. So i make comparisons easier like this.
        viewing_date: datetime = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        BrowserCookie.set_viewingdate_cookie(viewing_date)

        cls.TODAY = viewing_date
        cls.LOADED = True
