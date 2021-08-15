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
from src.schemas import ticket as ticket_schema
from src.models import tickets as ticket_model
from src.services.crud.base import CRUDBase


class TicketService(CRUDBase[ticket_model.Ticket, ticket_schema.TicketCreate, ticket_schema.TicketUpdate]):

    async def get(self, db: Session, item_id: UUID) -> Optional[ticket_model.Ticket]:
        """[summary]

        Args:
            db (Session): [description]
            item_id (UUID): [description]

        Returns:
            Optional[ticket_model.Ticket]: [description]
        """        
        return await super().get(db, item_id)

    async def list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ticket_model.Ticket]:
        """[summary]

        Args:
            db (Session): [description]
            skip (int): [description]
            limit (int): [description]

        Returns:
            List[ticket_model.Ticket]: [description]
        """        """  """
        return await super().list(db, skip=skip, limit=limit)

    async def create(self, db: Session, *, obj_in: ticket_schema.TicketCreate) -> ticket_model.Ticket:
        """[summary]

        Args:
            db (Session): [description]
            obj_in (ticket_schema.TicketCreate): [description]

        Returns:
            ticket_model.Ticket: [description]
        """        
        return await super().create(db, obj_in=obj_in)

    async def update(
        self, db: Session, *, db_obj: ticket_model.Ticket, obj_in: Union[ticket_schema.TicketUpdate, Dict[str, Any]]
    ) -> ticket_model.Ticket:
        """[summary]

        Args:
            db (Session): [description]
            db_obj (ticket_model.Ticket): [description]
            obj_in (Union[ticket_schema.TicketUpdate, Dict[str, Any]]): [description]

        Returns:
            ticket_model.Ticket: [description]
        """        
        return await super().update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove(self, db: Session, *, item_id: UUID) -> ticket_model.Ticket:
        """[summary]

        Args:
            db (Session): [description]
            item_id (UUID): [description]

        Returns:
            ticket_model.Ticket: [description]
        """        
        return await super().remove(db, item_id=item_id)


@lru_cache
def get_cluster_service(
    redis: Redis = Depends(get_redis),
) -> TicketService:
    return TicketService(
        ticket_model.Ticket,
        redis=redis,
    )
