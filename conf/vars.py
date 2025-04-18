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

# CLIENT INFO
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# MISC
JWT_SECRET = os.getenv("JWT_SECRET")
LOGGER_TO_USE = os.getenv("LOGGER_TO_USE", "local")
DEFAULT_CLIENT_HASH = "6f7517d93cdaaecaa64f3052d135539e"
