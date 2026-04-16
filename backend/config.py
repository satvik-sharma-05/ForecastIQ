from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB_NAME: str
    SECRET_KEY: str
    ENVIRONMENT: str = "development"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days
    JWT_ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
