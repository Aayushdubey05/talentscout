from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Integer
from src.core.settings import settings
from contextlib import asynccontextmanager
import uvicorn
from src.db.db import Base,engine, create_all_tables
from src.schema.user import Reg_of_users
from src.api.signup import signup_router

# import corus

origins = [
    "http://localhost.tiangolo.com",
    "https://locahost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8501"
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting the Server")
    # print(settings.DATABASE_URL)
    await create_all_tables(engine)     
    yield
    print(f"Stoping the server")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers = ["*"],
)


# Adding routers in the main file 
app.include_router(signup_router,prefix="/api",tags=["Auth"])
@app.get("/")
def home():
    return {"details" : "You are on Home page" }

if __name__ == "__main__":
    uvicorn.run("main:app",port=5000,host="127.0.0.1",reload=True)




