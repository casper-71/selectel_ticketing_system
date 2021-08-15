import enum

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Enum,
)

from src.db.postgresql import Base
from src.models.base_mixins import BaseMixin, TimestampMixin, AuditMixin
from src.models.history_meta import Versioned

# Этот импорт нужен для связи one-to-many для модели Ticket
from src.models.comments import Comment             # noqa: F401


class TicketStatus(enum.Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    ANSWERED = 'answered'
    WAIT_ANSWER = 'wait_answer'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_      # pylint: disable=no-member


class TicketMixin(TimestampMixin, AuditMixin):
    """ Ticket base model """

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    email = Column(String, nullable=False)
    status = Column(Enum(TicketStatus), nullable=False, default=TicketStatus.OPEN)


class Ticket(Versioned, Base, BaseMixin, TicketMixin):
    """  """

    @declared_attr
    def comment(cls):                               # pylint: disable=no-self-argument
        return relationship(
            "Comment",
            backref="ticket",
            cascade="all, delete"
        )
