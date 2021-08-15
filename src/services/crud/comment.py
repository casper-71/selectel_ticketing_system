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
from src.schemas import comment as comment_schema
from src.models import comments as comment_model
from src.services.crud.base import CRUDBase


class TicketService(CRUDBase[comment_model.Comment, comment_schema.CommentCreate, comment_schema.CommentUpdate]):

    async def get(self, db: Session, item_id: UUID) -> Optional[comment_model.Comment]:
        """[summary]

        Args:
            db (Session): [description]
            item_id (UUID): [description]

        Returns:
            Optional[comment_model.Comment]: [description]
        """        
        return await super().get(db, item_id)

    async def list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[comment_model.Comment]:
        """[summary]

        Args:
            db (Session): [description]
            skip (int): [description]
            limit (int): [description]

        Returns:
            List[comment_model.Comment]: [description]
        """        """  """
        return await super().list(db, skip=skip, limit=limit)

    async def create(self, db: Session, *, obj_in: comment_schema.CommentCreate) -> comment_model.Comment:
        """[summary]

        Args:
            db (Session): [description]
            obj_in (comment_schema.CommentCreate): [description]

        Returns:
            comment_model.Comment: [description]
        """        
        return await super().create(db, obj_in=obj_in)

    async def update(
        self, db: Session, *, db_obj: comment_model.Comment, obj_in: Union[comment_schema.CommentUpdate, Dict[str, Any]]
    ) -> comment_model.Comment:
        """[summary]

        Args:
            db (Session): [description]
            db_obj (comment_model.Comment): [description]
            obj_in (Union[comment_schema.CommentUpdate, Dict[str, Any]]): [description]

        Returns:
            comment_model.Comment: [description]
        """        
        return await super().update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove(self, db: Session, *, item_id: UUID) -> comment_model.Comment:
        """[summary]

        Args:
            db (Session): [description]
            item_id (UUID): [description]

        Returns:
            comment_model.Comment: [description]
        """        
        return await super().remove(db, item_id=item_id)


@lru_cache
def get_cluster_service(
    redis: Redis = Depends(get_redis),
) -> TicketService:
    return TicketService(
        comment_model.Comment,
        redis=redis,
    )
