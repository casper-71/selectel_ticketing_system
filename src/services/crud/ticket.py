from src.models.history_meta import versioned_session
from uuid import UUID
from functools import lru_cache
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
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
from src.schemas import ticket as ticket_schema
from src.models import tickets as ticket_model
from src.services.crud.base import CRUDBase


class TicketService(CRUDBase[ticket_model.Ticket, ticket_schema.TicketCreate, ticket_schema.TicketUpdate]):

    async def get(self, db: Session, item_id: UUID) -> Optional[ticket_model.Ticket]:
        """ Get ticket by ID

        Args:
            db (Session): SQLAlchemy Session
            item_id (UUID): ticket ID

        Returns:
            Optional[ticket_model.Ticket]: Ticket full data
        """
        ticket = await self.cache.get_from_cache(obj_id=str(item_id), obj_model=ticket_schema.Comment)
        if not ticket:
            ticket = await super().get(db, item_id)

            if ticket:
                await self.cache.put_to_cache(obj_model=ticket)

        return ticket

    async def list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ticket_model.Ticket]:
        """ List of tickets

        Args:
            db (Session): SQLAlchemy Session
            skip (int): page number
            limit (int): page limit

        Returns:
            List[ticket_model.Ticket]: List of tickets
        """        """  """
        return await super().list(db, skip=skip, limit=limit)

    async def create(self, db: Session, *, obj_in: ticket_schema.TicketCreate) -> ticket_model.Ticket:
        """Create a ticket

        Args:
            db (Session): SQLAlchemy Session
            obj_in (ticket_schema.TicketCreate): request parameters

        Returns:
            ticket_model.Ticket: Ticket full data
        """     
        versioned_session(db)
        data_in_obj = jsonable_encoder(obj_in)
        db_obj = ticket_model.Ticket(**data_in_obj)
        db_obj.status = obj_in.status

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    async def update(
        self, db: Session, *, db_obj: ticket_model.Ticket, obj_in: Union[ticket_schema.TicketUpdate, Dict[str, Any]]
    ) -> ticket_model.Ticket:
        """[summary]

        Args:
            db (Session): SQLAlchemy Session
            db_obj (ticket_model.Ticket): Database model of Ticket
            obj_in (Union[ticket_schema.TicketUpdate, Dict[str, Any]]): request parameters

        Returns:
            ticket_model.Ticket: Ticket full data
        """
        versioned_session(db)
        transactions_task = ticket_schema.TransactionStatus()
        ticket = None
        if type(obj_in) == dict:
            obj_in = ticket_schema.TicketUpdate(**obj_in)
        status_new = obj_in.status.value                      # type: ignore
        status_old = db_obj.status.value

        # Тикет создается в статусе “открыт”, может перейти в “отвечен” или “закрыт”, из
        # отвечен в “ожидает ответа” или “закрыт”, статус “закрыт” финальный (нельзя
        # изменить статус или добавить комментарий)

        if db_obj.status == ticket_model.TicketStatus.OPEN:
            if obj_in.status in transactions_task.open:   # type: ignore
                ticket = await super().update(db, db_obj=db_obj, obj_in=obj_in)

        if db_obj.status in [ticket_model.TicketStatus.ANSWERED, ticket_model.TicketStatus.WAIT_ANSWER]:
            if obj_in.status in transactions_task.answered:         # type: ignore
                ticket = await super().update(db, db_obj=db_obj, obj_in=obj_in)

        if ticket:
            await self.cache.delete_from_cache(obj_id=str(ticket.id))
            return ticket

        raise exceptions.TicketStatusNotAllowed(
            "Status Not Allowed",
            f"From status `{status_old}` to `{status_new}` Not Allowed"
        )

    async def remove(self, db: Session, *, item_id: UUID) -> ticket_model.Ticket:
        """[summary]

        Args:
            db (Session): SQLAlchemy Session
            item_id (UUID): ticket ID

        Returns:
            ticket_model.Ticket: Ticket full data
        """        
        ticket = await super().remove(db, item_id=item_id)
        await self.cache.delete_from_cache(obj_id=str(ticket.id))

        return ticket


@lru_cache
def get_ticket_service(
    redis: Redis = Depends(get_redis),
) -> TicketService:
    return TicketService(
        ticket_model.Ticket,
        redis=redis,
    )
