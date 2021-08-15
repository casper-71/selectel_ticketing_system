from uuid import UUID
from functools import lru_cache
from fastapi import Depends
from aioredis import Redis
from sqlalchemy.orm import Session
from typing import (
    Optional,
    List,
    Union,
    Dict,
    Any,
)

from src.db.redis import get_redis
from src.core import exceptions
from src.schemas import comment as comment_schema
from src.models import comments as comment_model, tickets
from src.services.crud.base import CRUDBase


class CommentService(CRUDBase[comment_model.Comment, comment_schema.CommentCreate, comment_schema.CommentUpdate]):

    async def get(self, db: Session, item_id: UUID) -> Optional[comment_model.Comment]:
        """ Get comment by ID

        Args:
            db (Session): SQLAlchemy Session
            item_id (UUID): comment ID

        Returns:
            Optional[comment_model.Comment]: Comment full data
        """        
        return await super().get(db, item_id)

    async def list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[comment_model.Comment]:
        """[summary]

        Args:
            db (Session): SQLAlchemy Session
            skip (int): page number
            limit (int): page limit

        Returns:
            List[comment_model.Comment]: List of comments
        """        """  """
        return await super().list(db, skip=skip, limit=limit)

    async def create(self, db: Session, *, obj_in: comment_schema.CommentCreate) -> comment_model.Comment:
        """Create a new comment

        Args:
            db (Session): SQLAlchemy Session
            obj_in (comment_schema.CommentCreate): request parameters

        Returns:
            comment_model.Comment: Comment full data
        """
        ticket = db.query(tickets.Ticket).filter_by(id=obj_in.ticket_id).one()

        # If ticket status is `Closed` comment won't create
        if ticket.status == tickets.TicketStatus.CLOSED:
            raise exceptions.TicketStatusNotAllowed(
                "Ticket Status Not Allowed",
                f"Comment Not Allowed in ticket status: {ticket.status.value}"
            )
        return await super().create(db, obj_in=obj_in)

    async def update(
        self, db: Session, *, db_obj: comment_model.Comment, obj_in: Union[comment_schema.CommentUpdate, Dict[str, Any]]
    ) -> comment_model.Comment:
        """Update comment

        Args:
            db (Session): SQLAlchemy Session
            db_obj (comment_model.Comment): Database Model
            obj_in (Union[comment_schema.CommentUpdate, Dict[str, Any]]): request parameters

        Returns:
            comment_model.Comment: Comment model
        """        
        return await super().update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove(self, db: Session, *, item_id: UUID) -> comment_model.Comment:
        """ Delete comment

        Args:
            db (Session): SQLAlchemy Session
            item_id (UUID): comment ID

        Returns:
            comment_model.Comment: Full data by Comment
        """        
        return await super().remove(db, item_id=item_id)


@lru_cache
def get_comment_service(
    redis: Redis = Depends(get_redis),
) -> CommentService:
    return CommentService(
        comment_model.Comment,
        redis=redis,
    )
