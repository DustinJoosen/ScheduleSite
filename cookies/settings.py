from datetime import datetime
from mongo.mongo import Mongo
from cookies.cookieencryption import substitution_decryption, substitution_encryption
from cookies.cookiegeneration import CookieGenerator


class Settings:
    TODAY: datetime = None
    LOADED: bool = False

    @classmethod
    def load(cls):
        # Set the cookies.
        encrypted_auth_cookie: str = Mongo.get_auth_document()

        # If the auth cookie is not yet set.
        if encrypted_auth_cookie is None:
            # Check if credentials are set.
            encrypted_credentials = Mongo.get_credentials_document()
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
            Mongo.set_auth_document(encrypted_cookie)

        # The API gives the time at 0. So i make comparisons easier like this.
        viewing_date: datetime = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        Mongo.set_viewingdate_document(viewing_date)

        cls.TODAY = viewing_date
        cls.LOADED = True
