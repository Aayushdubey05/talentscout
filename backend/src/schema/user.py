from pydantic import BaseModel, EmailStr
import typing
from src.db.db import get_db
class Reg_of_users(BaseModel):
    UserName: str
    Email: str
    Password: str

    class Config:
        from_attributes=True
    
class Non_reg_users(BaseModel):
    pass


class UserCreated:
    UserName: str
    Email: str 
    
    class Config:
        from_attributes = True


class Login(Reg_of_users):
    UserName: str | None
    Email: str | None
    Password: str 


class Message_from_llm(BaseModel):
    Response_from_AI : str

    class Config:
        orm_mode = True