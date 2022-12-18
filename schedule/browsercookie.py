
class Cookie:

    @classmethod
    def get_encrypted_cookies(cls) -> dict:
        # TODO: make this actually get from the cookies.
        return {
            "credentials": {
                "email": "S1184503@student.windesheim.nl",
                "password": "LGOYET.EABWzaheer3!"
            },
            "authcookie": None
        }

    @classmethod
    def set_cookie(cls, cookie: str):
        pass
