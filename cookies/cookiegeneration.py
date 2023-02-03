import asyncio
import pyppeteer
import time


class CookieGenerator:

    def __init__(self, username: str, pwd: str):
        self.username: str = username
        self.pwd: str = pwd

        self.cookie: str = None

    async def set_aspnet_cookie(self):
        starting_time: time = time.time()

        browser: Browser = await pyppeteer.launch(
            headless=False,
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False,
            args=["--no-sandbox"]
        )
        page: Page = await browser.newPage()

        try:
            # Set the url to the wip.
            await page.goto("https://wip.windesheim.nl")

            # Wait, enter the email address and click on the button.
            await page.waitForSelector("#i0116")
            await page.type("#i0116", self.username)
            await page.click("#idSIButton9")

            # Wait, enter the password and click on the button.
            await page.waitForSelector("#passwordInput")
            await page.type("#passwordInput", self.pwd)
            await page.click("#submitButton")

            # Wait and press the 'next' button.
            await page.waitForSelector("#idSIButton9")
            await page.click("#idSIButton9")

            print("authentication successfull")

            # Go to the azure website where the cookies are.
            await page.goto("https://windesheimapi.azurewebsites.net")
            await page.waitForSelector(".container")

            # Get the cookies.
            cookies: list = await page.cookies()
            for cookie in cookies:
                if cookie["name"] == ".AspNet.Cookies":
                    self.cookie = cookie["value"]

        except TimeoutError as ex:
            print("authentication was invalid.")
            await browser.close()
            return

        print(f"retrieval took {time.time() - starting_time} seconds")
        await browser.close()

    @staticmethod
    def init_acynchronous_method(action):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        tasks: list = [
            loop.create_task(action())
        ]

        try:
            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()
        except IOError as ex_1:
            print("an exception has occured(io)")
            print(ex_1)
        except OSError as ex_2:
            print("an exception has occured(os)")
            print(ex_2)
