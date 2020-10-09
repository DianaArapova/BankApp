from pydantic import BaseSettings
from sqlalchemy import create_engine


class DBSettings(BaseSettings):
    url: str

    class Config:
        env_prefix = "DATABASE_"

    def setup_db(self) -> None:
        from app.db import metadata

        metadata.bind = create_engine(self.url)
        metadata.create_all()


class AppSettings(BaseSettings):
    clear_holds_delay: float = 10 * 60

    class Config:
        env_prefix = "APP_"
