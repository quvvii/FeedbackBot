from environs import Env


env = Env()
env.read_env()

TOKEN = env.str("TELEGRAM_BOT_TOKEN")
ADMIN_ID = env.int("TELEGRAM_ADMIN_ID")
DB_URL = env.str("DATABASE_URL")

LOGGER_FORMAT = "[%(name)s] [%(asctime)s] [%(levelname)s] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
