import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)

class Settings:
    PROJECT_NAME:str = "Znanium"
    PROJECT_VERSION: str = "0.0.1"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL = (f"postgresql+asyncpg://{POSTGRES_USER}:"
                    f"{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:"
                    f"{POSTGRES_PORT}/{POSTGRES_DB}")
    SECRET_MANAGER_USER = os.environ.get("SECRET")
    SECRET = os.environ.get("SECRET_MANAGER_USER")

settings = Settings()