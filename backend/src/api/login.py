from fastapi import APIRouter, Depends, HTTPException, status
from src.schema.user import Reg_of_users, Login
from src.models.user import Users
from src.middleware.json_web_token import verify_password
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.db import get_db
from sqlalchemy import select
from pydantic import EmailStr
from fastapi.responses import RedirectResponse
login_router = APIRouter()

async def get_user_by_email(email: EmailStr,DB: AsyncSession = Depends(get_db)):
    result = await DB.execute(select(Users).where(Users.email == email))
    user = result.scalar_one_or_none()
    if user:
        return user.password
    return None

async def get_user_by_username(username: str,DB: AsyncSession= Depends(get_db)):
    result = await DB.execute(select(Users).where(Users.username == username))
    user = result.scalar_one_or_none()
    if user:
        return user.password
    return None


@login_router.post("/login/", response_model=str)
async def login(registered_users: Login, DB: AsyncSession=Depends(get_db)):
    try:
        username = Login.UserName
        email = Login.Email
        password = Login.Password

        if(username == None):
           got_registered_password = await get_user_by_email(email,DB)
           verify_password(password,got_registered_password)
           if(verify_password(password,got_registered_password) == False):
               return HTTPException(
                   status_code=status.HTTP_401_UNAUTHORIZED,
                   detail="Wrong Password"
               )
        
        if(email == None):
            got_registered_password = await get_user_by_username(username,DB)
            verify_password(password,got_registered_password)
            if(verify_password(password,got_registered_password) == False):
               return HTTPException(
                   status_code=status.HTTP_401_UNAUTHORIZED,
                   detail="Wrong Password"
               )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating Users"
        )
    
         

# This is incomplete I have to write the code for the returning the JSON, JWT token in the response 
    

            