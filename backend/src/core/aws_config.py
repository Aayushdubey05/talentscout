from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings
import os

base_path = Path(__file__).resolve().parent.parent.parent
env_path = base_path/".env"

load_dotenv(env_path)

## Access management Key of the AWS(For the AWS account)
class AWS_Config:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
