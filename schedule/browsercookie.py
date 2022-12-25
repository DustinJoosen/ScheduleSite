
class BrowserCookie:

    MOCK_COOKIE: dict = {
        "credentials": None,
        "authcookie": None
    }

    @classmethod
    def get_encrypted_cookies(cls) -> dict:
        # TODO: make this actually get from the cookies.
        return BrowserCookie.MOCK_COOKIE

    @classmethod
    def set_auth_cookie(cls, cookie: str):
        BrowserCookie.MOCK_COOKIE["authcookie"] = cookie

    @classmethod
    def set_credentials_cookie(cls, email: str, pwd: str):
        BrowserCookie.MOCK_COOKIE["credentials"] = {
            "email": email,
            "password": pwd
        }

    @classmethod
    def clear_auth_cookie(cls):
        BrowserCookie.MOCK_COOKIE["authcookie"] = ""
