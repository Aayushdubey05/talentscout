from datetime import datetime, timedelta, timezone
from typing import Annotated
from dotenv import load_dotenv
import jwt
from fastapi.security import OAuth2, OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from passlib.context import CryptContext
import os
from pathlib import Path
from src.schema.user import Reg_of_users
from src.db.db import get_db
from src.models.user import Users
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select



envpath = Path(__file__).parent.parent.parent/".env"
load_dotenv(envpath)
class jwtconfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# print(jwtconfig.SECRET_KEY)
# print(jwtconfig.ACCESS_TOKEN_EXPIRE_MINUTES)
# print(jwtconfig.ALGORITHM)
# Just to test the loading of the all the ENV variable 



# pydantic for the Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None 

class UserInDB(Reg_of_users):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Wirting the code for verification of the password + JWT token creation + getting the hashpassword(optional coz already wrote it. when it was needed)
def verify_password(plain_password , hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Optional(Not gonna use it anywhere)
def get_password_hash(password):
    return pwd_context.hash(password)

# Dont know why I am writing the get_user function just wrote it 
async def get_user(username: str,db : AsyncSession= Depends(get_db)):
    result = await db.execute(select(Users).where(Users.username == username))
    user = result.scalar_one_or_none()
    return user
    



# Authentication of users
async def authenticate_user(username: str, password: str, db: AsyncSession = Depends(get_db)):
    user_who_want_to_authenticate = await get_user(username , db)
    if not user_who_want_to_authenticate:
        return False
    if not verify_password(password, user_who_want_to_authenticate.password):
        return False
    return user_who_want_to_authenticate


# Creation of tokens and accessing of tokens 
def create_access_token(data: dict, expires_delta: timedelta| None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, jwtconfig.SECRET_KEY, algorithm=jwtconfig.ALGORITHM)
    return encode_jwt 


# Will use of for getting the current users
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentails",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token , jwtconfig.SECRET_KEY, algorithms=[jwtconfig.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data  = TokenData(username = username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username, db = Depends(get_db))
    if user is None:
        raise credentials_exception
    return user


# Will use for getting the user connceted to app/web service
async def get_current_active_user(
        current_user: Annotated[Reg_of_users, Depends(get_current_user)]):
    if  current_user.disabled:
        raise HTTPException(status_code=400, details="Inactive User")
    return current_user

