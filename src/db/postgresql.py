from typing import Optional
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from fastapi import Request

from src.core.config.app_settings import AppSettings


app_config = AppSettings()
database: Optional[Database] = None

engine = create_engine(app_config.db.pg_dsn)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

Base = declarative_base()


# Функция понадобится при внедрении зависимостей
def get_postgresql(request: Request) -> Request:
    return request.state.db
