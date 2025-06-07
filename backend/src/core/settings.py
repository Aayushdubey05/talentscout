from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings
import os

base_path = Path(__file__).resolve().parent.parent.parent
env_path = base_path/ ".env"

load_dotenv(env_path)
class Settings:
    USER = os.getenv("POSTGRE_USER")
    DATABASE_URL = os.getenv("POSTGRE_URL")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

settings = Settings()
# print(settings.USER)
# print(settings.DATABASE_URL)
# print(settings.OPENROUTER_API_KEY)