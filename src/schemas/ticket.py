import orjson

from datetime import datetime
from typing import List, Optional, Any
from uuid import UUID
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from src.models.tickets import TicketStatus
from src.schemas.comment import Comment


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    # https://pydantic-docs.helpmanual.io/usage/exporting_models/#custom-json-deserialisation
    return orjson.dumps(v, default=default).decode()    # pylint: disable=no-member


class TransactionStatus:

    @property
    def open(self) -> list:
        return [TicketStatus.ANSWERED, TicketStatus.CLOSED]

    @property
    def answered(self) -> list:
        return [TicketStatus.WAIT_ANSWER, TicketStatus.CLOSED]


# Shared properties
class TicketBase(BaseModel):
    status: TicketStatus = Field(
        default=TicketStatus.OPEN,
        description='''Тикет создается в статусе `open`, может перейти в `answered` или `closed`, из 
                    отвечен в `wait_answer` или `closed`, статус `closed` финальный (нельзя 
                    зменить статус или добавить комментарий)
                    ''',
    )

    class Config:
        json_loads = orjson.loads       # pylint: disable=no-member
        json_dumps = orjson_dumps
        allow_population_by_field_name = True


# Properties to receive on Ticket creation
class TicketCreate(TicketBase):
    title: str
    description: Optional[str]
    email: EmailStr

    created_by: str
    updated_by: Optional[str] 

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.updated_by = self.created_by


class TicketUpdate(TicketBase):
    updated_by: str


class TicketInDBBase(TicketBase):
    id: Optional[UUID]
    title: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class Ticket(TicketInDBBase):
    pass


class TicketFull(TicketInDBBase):
    updated_at: Optional[datetime]
    description: Optional[str]
    comment: List[Comment] = Field(..., alias='comments')
