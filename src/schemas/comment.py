import orjson

from typing import Optional
from uuid import UUID
from pydantic import (
    BaseModel,
    EmailStr,
)


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    # https://pydantic-docs.helpmanual.io/usage/exporting_models/#custom-json-deserialisation
    return orjson.dumps(v, default=default).decode()    # pylint: disable=no-member


# Shared properties
class CommentBase(BaseModel):
    body: Optional[str]

    class Config:
        json_loads = orjson.loads       # pylint: disable=no-member
        json_dumps = orjson_dumps
        allow_population_by_field_name = True


class CommentCreate(CommentBase):
    email: EmailStr
    body: str
    ticket_id: UUID

    created_by: str
    updated_by: str


class CommentUpdate(CommentBase):
    body: str
    updated_by: str


class CommentInDBBase(CommentBase):
    id: Optional[UUID]
    email: Optional[EmailStr]

    class Config:
        orm_mode = True


class Comment(CommentInDBBase):
    ticket_id: Optional[UUID]


class CommentFull(CommentInDBBase):
    created_by: Optional[str]
    updated_by: Optional[str]
