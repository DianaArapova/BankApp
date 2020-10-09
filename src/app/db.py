import sqlalchemy as sa
from databases import Database

from app.settings import DBSettings

metadata = sa.MetaData()

accounts = sa.Table(
    "account",
    metadata,
    sa.Column("account_id", sa.Integer, primary_key=True),
    sa.Column("account_uuid", sa.String(40), unique=True, nullable=False, index=True),
    sa.Column("full_name", sa.String(100), nullable=False),
    sa.Column("balance", sa.Integer, nullable=False),
    sa.Column("holds", sa.Integer, nullable=False),
    sa.Column("status", sa.Boolean, nullable=False),
)

database = Database(DBSettings().url)
