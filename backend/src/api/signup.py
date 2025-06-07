from fastapi import FastAPI, openapi, APIRouter, Depends, requests,status, HTTPException
from src.db.db import get_db
from src.models.user import Users
from src.schema.user import Reg_of_users, Non_reg_users,UserCreated
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

signup_router = APIRouter()


# Signup code is written overhere 
# we love writing signup code 
@signup_router.post("/reg",status_code=status.HTTP_201_CREATED)
async def signup(New_user: Reg_of_users, db : AsyncSession = Depends(get_db)):
    try:
        existing_user = await db.execute(
            select(Users).where(
                (Users.username == New_user.UserName) | (Users.email == New_user.Email)
            )
        )

        if existing_user.scalar_one_or_none():
            raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Username or email already exist"
        )

        db_users = Users(
            username = New_user.UserName,
            email = New_user.Email,
            password = pwd_context.hash(New_user.Password)
        )

        db.add(db_users)
        await db.commit()
        await db.refresh(db_users)

        return {"status":"success","detail":"User Created"}
    
    except Exception as error:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating Users {error}" 
        )
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"registration failed {e}")




