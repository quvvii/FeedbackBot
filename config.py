from environs import Env


env = Env()
env.read_env()

TOKEN = env.str("TELEGRAM_BOT_TOKEN")
ADMIN_ID = env.int("TELEGRAM_ADMIN_ID")
DB_URL = "sqlite:///app/data/db.sqlite3"

LOGGER_FORMAT = "[%(name)s] [%(asctime)s] [%(levelname)s] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
