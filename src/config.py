from dotenv import load_dotenv
import os

load_dotenv()

MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
MAX_BOT_USERNAME = os.getenv("MAX_BOT_USERNAME")

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_AUTO_CREATE = os.getenv("DB_AUTO_CREATE", "1").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
