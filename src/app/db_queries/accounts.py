from app.models.accounts import AccountSchema, AccountDBSchema
from app.db import accounts, database

from uuid import uuid4
from typing import List, Optional


async def create(account: AccountSchema) -> str:
    query = accounts.insert(inline=True).values(
        account_uuid=str(uuid4()),
        full_name=account.full_name,
        balance=account.balance,
        holds=account.holds,
        status=account.status,
    ).returning(accounts.c.account_uuid)

    return await database.execute(query=query)


async def update(account: AccountDBSchema) -> str:
    query = (
        accounts
        .update()
        .where(account.account_uuid == accounts.c.account_uuid)
        .values(
            full_name=account.full_name,
            balance=account.balance,
            holds=account.holds,
            status=account.status,
        )
        .returning(accounts.c.account_uuid)
    )
    return await database.execute(query=query)


async def clear_holds() -> None:
    query = (
        accounts
        .update()
        .values(
            balance=accounts.c.balance-accounts.c.holds,
            holds=0,
        )
    )
    await database.execute(query=query)


async def get(account_uuid: str) -> Optional[AccountDBSchema]:
    query = accounts.select().where(account_uuid == accounts.c.account_uuid)
    result = await database.fetch_one(query=query)
    if not result:
        return None
    return AccountDBSchema(**result)


async def get_all() -> List[AccountDBSchema]:
    query = accounts.select()
    return await database.fetch_all(query)
