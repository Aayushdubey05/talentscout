from pydantic import BaseModel
import typing
from typing import Optional
from .user import UserCreated
class resume_storage(BaseModel):
    ParentId: int
    ResumeId: str
    Path: Optional[str]

    
