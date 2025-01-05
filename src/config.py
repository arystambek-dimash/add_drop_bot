from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int = 5432

    TELEGRAM_TOKEN: str

    class Config:
        env_file = BASE_DIR / ".env"


def get_settings() -> Settings:
    return Settings()
