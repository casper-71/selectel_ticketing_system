from pydantic import BaseModel
from typing import (
    TypeVar,
    Optional,
    List,
    Dict,
    Any,
)

from src.models.base_mixins import BaseMixin
from src.core.config.app_settings import AppSettings


app_config = AppSettings()
ModelType = TypeVar("ModelType", bound=BaseMixin)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


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

    async def put_to_cache(self, obj_model: ModelType):
        """[summary]

        Args:
            obj_model (ModelType): [description]
        """        

    async def get_list_from_cache(self, objs_cache_id: str, obj_model: ModelType) -> Optional[List[ModelType]]:
        """[summary]

        Args:
            objs_cache_id (str): [description]
            obj_model (ModelType): [description]

        Returns:
            Optional[List[ModelType]]: [description]
        """        

    async def put_list_to_cache(self, objs_cache_id: str, objs: List[Dict[str, Any]]):
        """[summary]

        Args:
            objs_cache_id (str): [description]
            objs (List[Dict[str, Any]]): [description]
        """        

    async def delete_from_cache(self, obj_id: str):
        """[summary]

        Args:
            obj_id (str): [description]
        """        
        await self.db.delete(obj_id)
