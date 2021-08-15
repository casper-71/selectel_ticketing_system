import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr


class BaseMixin:
    """
        Базовая модель. Добавляет во всех наследников поле id и атрибут
        __tablename__ который заполняется автоматически.
        Имя таблицы берется из названия класса, переводится в нижний регистр и преобразуется в множественное число.
    """

    @declared_attr
    def __tablename__(cls):     # pylint: disable=no-self-argument
        return f"{cls.__name__.lower()}s"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class TimestampMixin:
    """
    Mixin который добавляет в другие модели поля:
    created_at - дата создания
    updated_at - дата последнего обновления
    Поля заполняются автоматически.
    """

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class AuditMixin:
    """
        Mixin который добавляет в другие модели поля:
        created_by - кем создано
        updated_by - кем обновлено
    """
    created_by = Column(Text, nullable=False)
    updated_by = Column(Text, nullable=False)
