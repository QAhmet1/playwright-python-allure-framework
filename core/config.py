import os
from dotenv import load_dotenv

env = os.getenv("TEST_ENV", "qa")
load_dotenv(f".env.{env}")

class Config:
    BASE_URL = os.getenv("BASE_URL")
    USER_NAME = os.getenv("STANDARD_USER")
    PASSWORD = os.getenv("PASSWORD")
    TIMEOUT = 30000