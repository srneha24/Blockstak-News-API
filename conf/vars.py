import os
from dotenv import load_dotenv


load_dotenv()

# NEWS API
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# POSTGRES DB
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# MISC
JWT_SECRET = os.getenv("JWT_SECRET")
LOGGER_TO_USE = os.getenv("LOGGER_TO_USE", "local")
