from app.client.browser import BrowserSession
from app.config import settings


class UrjaClient:

    def __init__(self):

        self.base_url = settings.URJA_URL.rstrip("/")
        self.username = settings.USERNAME
        self.password = settings.PASSWORD

        self.browser = BrowserSession()

        self.logged_in = False



    async def login(self):

        if self.logged_in:
            return True


        await self.browser.start()

        page = self.browser.page


        await page.goto(
            f"{self.base_url}/login",
            wait_until="networkidle"
        )


        print("LOGIN PAGE OPENED")
        print("Please login manually in the browser window...")


        # Optional: fill credentials
        await page.fill(
            "input[name='email']",
            self.username
        )


        await page.fill(
            "input[name='password']",
            self.password
        )


        # Wait until user login completes
        try:

            await page.wait_for_url(
                "**/meters",
                timeout=120000   # 2 minutes
            )


        except Exception:

            print("Login timeout")

            return False



        print(
            "LOGIN SUCCESS:",
            page.url
        )


        print(
            "COOKIES:",
            await self.browser.context.cookies()
        )


        self.logged_in = True


        return True




    async def get_meters(self):

        success = await self.login()


        if not success:

            return {
                "error": "login failed"
            }


        page = self.browser.page

        api_response = {}



        async def capture(response):

            if "/portal/meters/search" in response.url:

                try:

                    api_response.update(
                        await response.json()
                    )

                except Exception:

                    pass



        page.on(
            "response",
            capture
        )


        await page.reload()

        await page.wait_for_timeout(
            3000
        )


        return api_response





    async def get_meter_geo(
        self,
        meter_id: str
):

        success = await self.login()

        if not success:
            return {
                "error": "login failed"
            }


        page = self.browser.page


        await page.goto(
            f"{self.base_url}/meters/{meter_id}",
            wait_until="networkidle"
        )


        await page.wait_for_timeout(3000)


        html = await page.content()


        import re


        coordinates = re.findall(
            r'(-?\d+\.\d+),\s*(-?\d+\.\d+)',
            html
        )


        latitude = None
        longitude = None


        if coordinates:

            latitude = coordinates[0][0]
            longitude = coordinates[0][1]


        return {

            "latitude": latitude,

            "longitude": longitude

        }





    async def get_meter_energy(
            self,
            meter_id: str
    ):


        success = await self.login()


        if not success:

            return {
                "error": "login failed"
            }



        page = self.browser.page

        energy_data = {}



        async def capture(response):

            try:

                content_type = response.headers.get(
                    "content-type",
                    ""
                )


                if "json" in content_type:

                    data = await response.json()

                    if isinstance(data, dict):

                        energy_data.update(data)


            except Exception:

                pass



        page.on(
            "response",
            capture
        )


        await page.goto(

            f"{self.base_url}/meters/{meter_id}",

            wait_until="networkidle"

        )


        await page.wait_for_timeout(
            5000
        )


        return energy_data





    async def get_meter(
            self,
            meter_id: str
    ):


        success = await self.login()


        if not success:

            return {
                "error": "login failed"
            }



        return {

            "meter": {

                "meterId": meter_id

            },

            "geo": await self.get_meter_geo(
                meter_id
            ),

            "energy": await self.get_meter_energy(
                meter_id
            )

        }





    async def close(self):

        await self.browser.close()