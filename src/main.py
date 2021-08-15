import logging
import aioredis
import databases
import uvicorn

from logging import config as logging_config
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse

from src.core import logger
from src.core.config.app_settings import AppSettings
from src.db import redis, postgresql

# Применяем настройки логирования
logging_config.dictConfig(logger.LOGGING)

# Настройки приложения
app_config = AppSettings()


app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=app_config.app_name,
    # Адрес документации в красивом интерфейсе
    redoc_url='/api/redoc',
    docs_url='/api/openapi',
    # Адрес документации в формате OpenAPI
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    version=app_config.app_version,
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = postgresql.SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.on_event('startup')
async def startup():
    # Подключаемся к базам при старте сервера
    # Подключиться можем при работающем event-loop
    # Поэтому логика подключения происходит в асинхронной функции
    redis.pool = aioredis.ConnectionPool.from_url(
        app_config.redis_db.cache_dsn,
        decode_responses=True,
    )

    redis.redis = aioredis.Redis(connection_pool=redis.pool)
    postgresql.database = await databases.Database(app_config.db.pg_dsn).connect()


@app.on_event('shutdown')
async def shutdown():
    # Отключаемся от баз при выключении сервера
    await redis.pool.disconnect()
    await postgresql.database.disconnect()


if __name__ == '__main__':
    # Приложение должно запускаться с помощью команды
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # Но таким способом проблематично запускать сервис в дебагере,
    # поэтому сервер приложения для отладки запускаем здесь
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=logger.LOGGING,
        log_level=logging.DEBUG,
    )
