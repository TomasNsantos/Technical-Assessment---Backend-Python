from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    API_KEY: str = "your_secret_key"
    API_VERSION: str = "v1"

    class Config:
        env_file = ".env"

settings = Settings()