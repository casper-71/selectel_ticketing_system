from typing import Optional
from pydantic import (
    BaseSettings,
    RedisDsn,
)


class RedisSettings(BaseSettings):
    host: str
    port: str
    cache_dsn: Optional[RedisDsn]

    CACHE_EXPIRE_IN_SECONDS: int = 300

    def __init__(self, **data):
        super(RedisSettings, self).__init__(**data)
        self.cache_dsn = f"redis://{self.host}:{self.port}/0"

    class Config:
        env_prefix = "REDIS_"
