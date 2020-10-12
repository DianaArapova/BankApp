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

    @staticmethod
    def teardown_db() -> None:
        from app.db import metadata

        metadata.drop_all()


class AppSettings(BaseSettings):
    clear_holds_delay: int = 10 * 60

    class Config:
        env_prefix = "APP_"
