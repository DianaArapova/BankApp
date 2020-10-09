import sqlalchemy as sa
from databases import Database
from sqlalchemy import Boolean, Column, Integer, MetaData, String

from app.settings import DBSettings

metadata = MetaData()

accounts = sa.Table(
    "account",
    metadata,
    Column("account_id", Integer, primary_key=True),
    Column("account_uuid", String(40), unique=True, nullable=False, index=True),
    Column("full_name", String(100), nullable=False),
    Column("balance", Integer, nullable=False),
    Column("holds", Integer, nullable=False),
    Column("status", Boolean, nullable=False),
)

database = Database(DBSettings().url)
