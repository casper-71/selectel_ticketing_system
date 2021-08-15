import json
import pickle

from fastapi import Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import (
    TypeVar,
    Optional,
    List,
    Dict,
    Any,
)

from src.db.postgresql import Base
from src.core.config.app_settings import AppSettings


app_config = AppSettings()
ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


# Класс для параметров страницы: число объектов и номер страницы
class Page:
    def __init__(
            self,
            size: int = Query(10, alias='page[size]', gt=0, le=100),
            number: int = Query(0, alias='page[number]', gt=0),
    ):
        self.size = size
        self.number = number


async def prepare_list_items_to_cache(objs: List[SchemaType]):
    """
    Transform non-valid data from Pydantic model to Redis
    :param objs: list of pydantic models
    :return: list of transformed data
    """
    obj_list = []
    types = [str, list, int]
    for obj in objs:
        obj = obj.dict()                                # type: ignore
        for key in obj.keys():                          # type: ignore
            if isinstance(types, type(obj[key])):       # type: ignore
                obj[key] = str(obj[key])                # type: ignore

        obj_list.append(obj)

    return obj_list


# Класс отвечающий за запись и получение данных из кэша
class Cache:
    def __init__(self, db):
        self.db = db

    async def get_from_cache(self, obj_id: str, obj_model: ModelType):
        """[summary]

        Args:
            obj_id (str): [description]
            obj_model (ModelType): [description]
        """
        data = await self.db.get(obj_id)
        if not data:
            return None

        return obj_model.parse_obj(pickle.loads(data))

    async def put_to_cache(self, obj_model: ModelType):
        """[summary]

        Args:
            obj_model (ModelType): [description]
        """
        await self.db.set(
            f'{obj_model.__tablename__.lower()}_{obj_model.id}',
            pickle.dumps(jsonable_encoder(obj_model)),
        )
        await self.db.expire(
            name=f'{obj_model.__tablename__.lower()}_{obj_model.id}',
            time=app_config.redis_db.CACHE_EXPIRE_IN_SECONDS
        )

    async def get_list_from_cache(self, objs_cache_id: str, obj_model: ModelType) -> Optional[List[ModelType]]:
        """[summary]

        Args:
            objs_cache_id (str): [description]
            obj_model (ModelType): [description]

        Returns:
            Optional[List[ModelType]]: [description]
        """   
        objs = await self.db.get(objs_cache_id)
        if not objs:
            return None

        objs = json.loads(objs)
        new_objs = []
        for obj in objs:
            new_objs.append(obj_model.parse_raw(json.dumps(obj)))
        return new_objs     

    async def put_list_to_cache(self, objs_cache_id: str, objs: List[Dict[str, Any]]):
        """[summary]

        Args:
            objs_cache_id (str): [description]
            objs (List[Dict[str, Any]]): [description]
        """   
        await self.db.set(
            objs_cache_id,
            json.dumps(objs),
        )    

        await self.db.expire(
            name=objs_cache_id,
            time=app_config.redis_db.CACHE_EXPIRE_IN_SECONDS,
        ) 

    async def delete_from_cache(self, obj_id: str):
        """[summary]

        Args:
            obj_id (str): [description]
        """        
        await self.db.delete(obj_id)
