import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"

settings = Settings()
