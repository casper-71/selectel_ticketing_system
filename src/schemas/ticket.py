import orjson

from typing import List, Optional
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


# Shared properties
class TicketBase(BaseModel):
    status: TicketStatus = TicketStatus.OPEN

    class Config:
        json_loads = orjson.loads       # pylint: disable=no-member
        json_dumps = orjson_dumps
        allow_population_by_field_name = True


# Properties to receive on Ticket creation
class TicketCreate(TicketBase):
    title: str
    description: Optional[str]
    email: EmailStr


class TicketUpdate(TicketBase):
    pass


class TicketInDBBase(TicketBase):
    id: Optional[UUID]
    title: Optional[str]

    class Config:
        orm_mode = True


class Ticket(TicketInDBBase):
    pass


class TicketFull(TicketInDBBase):
    description: Optional[str]
    comment: List[Comment] = Field(..., alias='comments')
