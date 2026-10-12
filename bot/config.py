from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timezone, timedelta


class Settings(BaseSettings):
    bot_token: str
    proxy_url: str | None = None
    owner_id: int
    tz_offset: int = 3
    db_path: str = "data/bot.db"
    log_level: str = "INFO"

    @property
    def tz(self) -> timezone:
        return timezone(timedelta(hours=self.tz_offset))

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
