from pathlib import Path

from alembic import context
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int = 5432

    TELEGRAM_TOKEN: str

    REDIS_HOST: str
    REDIS_DB: int
    REDIS_PORT: int

    class Config:
        env_file = BASE_DIR / ".env"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()