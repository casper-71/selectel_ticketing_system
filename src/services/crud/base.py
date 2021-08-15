from typing import TypeVar, Generic, Type, Optional, List, Union, Dict, Any
from uuid import UUID

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from aioredis import Redis

from src.core.modules import Cache
from src.models.base_mixins import BaseMixin

ModelType = TypeVar("ModelType", bound=BaseMixin)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], redis: Redis = None):
        """
            CRUD object with default methods to Create, Read, Update, Delete (CRUD).
            **Parameters**
            * `model`: A SQLAlchemy model class
            * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.redis = redis
        self.cache = Cache(db=self.redis)

    async def get(self, db: Session, item_id: UUID) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == item_id).first()

    async def list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip * limit).limit(limit).all()

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())       # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data.get(field))

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def remove(self, db: Session, *, item_id: UUID) -> ModelType:
        remove_db_obj = db.query(self.model).get(item_id)
        db.delete(remove_db_obj)
        db.commit()
        return remove_db_obj
