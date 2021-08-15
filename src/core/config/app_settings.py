from pydantic import BaseSettings, Field

from src.core.config.database_settings import DBSettings
from src.core.config.redis_settings import RedisSettings


class AppSettings(BaseSettings):
    app_name: str = "Ticketing Service"
    app_version: str = "0.1.0"

    db: DBSettings = Field(default_factory=DBSettings)
    redis_db: RedisSettings = Field(default_factory=RedisSettings)


# Функция понадобится при внедрении зависимостей
def get_settings() -> AppSettings:
    return AppSettings()
