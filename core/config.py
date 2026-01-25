import os
from dotenv import load_dotenv

# Determine environment (default: qa)
env = os.getenv("TEST_ENV", "qa").lower()

# Load local .env file if it exists
env_file = f".env.{env}"
if os.path.exists(env_file):
    load_dotenv(env_file)

class Config:
    """
    Configuration class that pulls from environment variables.
    """
    BASE_URL = os.getenv("BASE_URL")
    USER_NAME = os.getenv("STANDARD_USER")
    PASSWORD = os.getenv("PASSWORD")
    TIMEOUT = int(os.getenv("TIMEOUT", 30000))