from typing import List, Optional
from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from app.db import accounts, database
from app.models.accounts import (
    AccountDBSchema,
    AccountSchema,
    ChangeAccountBalanceRequest,
    CloseAccountRequest,
)


async def create(account: AccountSchema) -> str:
    create_retry_count = 1000

    for retry_count in range(create_retry_count):
        try:
            query = (
                accounts.insert(inline=True)
                .values(
                    account_uuid=str(uuid4()),
                    full_name=account.full_name,
                    balance=account.balance,
                    holds=account.holds,
                    status=account.status,
                )
                .returning(accounts.c.account_uuid)
            )

            return await database.execute(query=query)
        except IntegrityError:
            if retry_count + 1 < create_retry_count:
                continue
            else:
                raise


async def update(account: AccountDBSchema) -> str:
    query = (
        accounts.update()
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


async def decrease_balance(request: ChangeAccountBalanceRequest) -> str:
    query = (
        accounts.update()
        .where(request.account_uuid == accounts.c.account_uuid)
        .where(accounts.c.status)
        .where(request.change_amount <= accounts.c.balance - accounts.c.holds)
        .values(
            holds=accounts.c.holds + request.change_amount,
        )
        .returning(accounts.c.account_uuid)
    )

    return await database.execute(query=query)


async def increase_balance(request: ChangeAccountBalanceRequest) -> str:
    query = (
        accounts.update()
        .where(request.account_uuid == accounts.c.account_uuid)
        .where(accounts.c.status)
        .values(
            balance=accounts.c.balance + request.change_amount,
        )
        .returning(accounts.c.account_uuid)
    )

    return await database.execute(query=query)


async def close_account(request: CloseAccountRequest) -> str:
    query = (
        accounts.update()
        .where(request.account_uuid == accounts.c.account_uuid)
        .where(accounts.c.status)
        .values(
            status=False,
        )
        .returning(accounts.c.account_uuid)
    )

    return await database.execute(query=query)


async def clear_holds() -> None:
    query = accounts.update().values(
        balance=accounts.c.balance - accounts.c.holds,
        holds=0,
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
