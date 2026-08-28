from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    JWT_SECRET_KEY: str

    SERVICE_DOMAIN: HttpUrl

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8"
    )

    @property
    def database_url(self):
        # Формат: dialect+driver://username:password@host:port/database
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
