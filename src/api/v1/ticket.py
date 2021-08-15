from typing import List, Optional
from uuid import UUID
from http import HTTPStatus

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from src.core import exceptions
from src.core.modules import Page
from src.db.postgresql import get_postgresql
from src.schemas.ticket import (
    Ticket,
    TicketFull,
    TicketCreate,
    TicketUpdate,
)
from src.services.crud.ticket import TicketService, get_ticket_service


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get("/{ticket_id}", response_model=TicketFull)
async def get_ticket(
    *,
    ticket_id: UUID,
    db: Session = Depends(get_postgresql),
    service: TicketService = Depends(get_ticket_service),
) -> Optional[TicketFull]:
    """Get ticket by ID

    Args:  
        ticket_id (UUID): ticket ID  

    Returns:  
        Optional[TicketFull]: Ticket full data
    """   
    ticket = await service.get(db=db, item_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='ticket not found')

    return ticket     


@router.get("/", response_model=List[Ticket])
async def list_tickets(
    *,
    page: Page = Depends(),
    db: Session = Depends(get_postgresql),
    service: TicketService = Depends(get_ticket_service),
) -> Optional[List[Ticket]]:
    """Get tickets list

    Args:  
        page (Page, optional): page size and page limits  

    Returns:  
        Optional[List[Ticket]]: List of tickets
    """
    tickets = await service.list(db, skip=page.number, limit=page.size)
    if not tickets:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='tickets not found')

    return tickets      # type: ignore


@router.post("/", response_model=TicketFull)
async def create_ticket(
    *,
    ticket_in: TicketCreate,
    db: Session = Depends(get_postgresql),
    service: TicketService = Depends(get_ticket_service),
) -> TicketFull:
    """Create a new ticket

    Args:
        ticket_in (TicketCreate): body request

    Returns:
        TicketFull: Ticket full data
    """

    return await service.create(db, obj_in=ticket_in)


@router.put("/{ticket_id}", response_model=TicketFull)
async def update_ticket(
    *,
    ticket_id: UUID,
    ticket_in: TicketUpdate,
    db: Session = Depends(get_postgresql),
    service: TicketService = Depends(get_ticket_service),
) -> Optional[TicketFull]:
    """Update ticket

    Args:
        ticket_id (UUID): ticket ID  

    Returns:
        Optional[TicketFull]: Ticket full data
    """
    ticket = await service.get(db, item_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='ticket not found')

    try:
        return await service.update(db, db_obj=ticket, obj_in=ticket_in)
    except exceptions.TicketStatusNotAllowed as error:
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED, detail=f"{error.message}")


@router.delete("/{ticket_id}", response_model=TicketFull)
async def delete_ticket(
    *,
    ticket_id: UUID,
    db: Session = Depends(get_postgresql),
    service: TicketService = Depends(get_ticket_service),
) -> TicketFull:
    """Delete a ticket

    Args:
        ticket_id (UUID): ticket ID  

    Returns:
        TicketFull: Ticket full data
    """
    ticket = await service.get(db, item_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='ticket not found')

    return await service.remove(db, item_id=ticket_id)
