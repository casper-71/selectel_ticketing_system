import aioredis


redis: aioredis.Redis = None            # type: ignore
pool: aioredis.ConnectionPool = None    # type: ignore


# Функция понадобится при внедрении зависимостей
async def get_redis() -> aioredis.Redis:
    return redis
