from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from .db import get_db
from sqlalchemy import select
from src.models.user import Users, Message, Conversation
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
UpdateMessageOfLLModel = TypeVar("UpdateMessageOfLLModel", bound=str)
ConversationUpdates = TypeVar("ConversationUpdates", bound=int)
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateMessageOfLLModel, ConversationUpdates]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, DB: AsyncSession, id: Any) -> Optional[ModelType]:
        result =  await DB.execute(
            select(self.model).where(self.model.id == id )
        )
        return result.scalar_one_or_none
    
    
    async def get_multi(self, DB: AsyncSession, *, skip: int = 0, limit: int=100 ) -> List[ModelType]:
        result = await DB.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalar().all()
    
    async def create(self, DB : AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        DB.add(db_obj)
        await DB.commit()
        await DB.refresh(db_obj)
        return db_obj
    
    # async def set_context_window(self, DB: AsyncSession):

crud = CRUDBase([Users])
    