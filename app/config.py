from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    api_key: str = Field("your_secret_key", env="API_KEY")
    api_version: str = Field("v1", env="API_VERSION")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()