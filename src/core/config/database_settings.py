from pydantic import (
    BaseSettings,
    PostgresDsn,
)


class DBSettings(BaseSettings):
    pg_dsn: PostgresDsn

    class Config:
        env_prefix = 'DATABASE_'
