import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.URJA_URL = os.getenv("URJA_URL")
        self.USERNAME = os.getenv("USERNAME")
        self.PASSWORD = os.getenv("PASSWORD")


settings = Settings()