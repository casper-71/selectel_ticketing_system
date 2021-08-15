from typing import Optional
from uuid import UUID
from http import HTTPStatus

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from src.core import exceptions
from src.db.postgresql import get_postgresql
from src.schemas.comment import (
    CommentFull,
    CommentCreate,
)
from src.services.crud.comment import CommentService, get_comment_service


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get("/{comment_id}", response_model=CommentFull)
async def get_comment(
    *,
    comment_id: UUID,
    db: Session = Depends(get_postgresql),
    service: CommentService = Depends(get_comment_service),
) -> Optional[CommentFull]:
    """[summary]

    Args:  
        Comment_id (UUID): [description]  

    Returns:  
        Optional[CommentFull]: [description]  
    """   
    comment = await service.get(db=db, item_id=comment_id)
    if not comment:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Comment not found')

    return comment     


@router.post("/", response_model=CommentFull)
async def create_comment(
    *,
    comment_in: CommentCreate,
    db: Session = Depends(get_postgresql),
    service: CommentService = Depends(get_comment_service),
) -> CommentFull:
    """[summary]

    Args:
        Comment_in (CommentCreate): [description]

    Returns:
        CommentFull: [description]
    """

    try:
        return await service.create(db, obj_in=comment_in)
    except exceptions.TicketStatusNotAllowed as error:
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED, detail=f"{error.message}")


@router.delete("/{comment_id}", response_model=CommentFull)
async def delete_comment(
    *,
    comment_id: UUID,
    db: Session = Depends(get_postgresql),
    service: CommentService = Depends(get_comment_service),
) -> CommentFull:
    """[summary]

    Args:
        Comment_id (UUID): [description]

    Returns:
        CommentFull: [description]
    """
    comment = await service.get(db, item_id=comment_id)
    if not comment:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Comment not found')

    return await service.remove(db, item_id=comment_id)
