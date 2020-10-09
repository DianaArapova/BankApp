import asyncio
import logging

from fastapi import HTTPException

import app.db_queries.accounts as db_query_executor
from app.models.accounts import (AccountDBSchema, AccountResponse,
                                 AccountSchema, ChangeAccountBalanceRequest,
                                 CloseAccountRequest, OpenAccountRequest)

logger = logging.getLogger(__name__)


async def create_account(request: OpenAccountRequest) -> AccountResponse:
    logger.info(f"Creating account (request: {request})")

    requested_account = AccountSchema(
        full_name=request.full_name,
        balance=0,
        status=True,
        holds=0,
    )
    account_uuid = await db_query_executor.create(requested_account)
    account = AccountDBSchema(account_uuid=account_uuid, **requested_account.dict())

    logger.info(f"Created account (account: {account})")

    return AccountResponse(
        result=True,
        addition=[account],
        description={"message": "Account created"},
    )


async def close_account(request: CloseAccountRequest) -> AccountResponse:
    logger.info(f"Closing account (request: {request})")

    account = await db_query_executor.get(request.account_uuid)
    raise_http_exception_on_invalid_accounts(account, request.account_uuid)

    account.status = False
    await db_query_executor.update(account)

    logger.info(f"Closed account (account: {account})")

    return AccountResponse(
        result=True,
        addition=[account],
        description={"message": f"Account {request.account_uuid} closed"},
    )


async def add_to_balance(request: ChangeAccountBalanceRequest) -> AccountResponse:
    logger.info(f"Increasing balance (request: {request})")

    account = await db_query_executor.get(request.account_uuid)
    raise_http_exception_on_invalid_accounts(account, request.account_uuid)

    account.balance += request.change_amount
    await db_query_executor.update(account)

    logger.info(f"Increased balance (account: {account})")

    return AccountResponse(
        result=True,
        addition=[account],
        description={
            "message": f"Add {request.change_amount} to account {request.account_uuid} balance"
        },
    )


async def substract_balance(request: ChangeAccountBalanceRequest) -> AccountResponse:
    logger.info(f"Try decreasing balance (request: {request})")

    account = await db_query_executor.get(request.account_uuid)
    raise_http_exception_on_invalid_accounts(account, request.account_uuid)

    result = account.balance - account.holds - request.change_amount
    if result < 0:
        logger.info(
            f"Decreasing failed (account_uuid: {request.account_uuid}, expected_balance: {result})"
        )
        return AccountResponse(
            result=False,
            addition=[account],
            description={
                "message": f"Operation is prohibited, there is not enough money in the account {request.account_uuid}"
            },
        )

    account.holds += request.change_amount
    await db_query_executor.update(account)

    logger.info(f"Decreased balance (account: {account})")

    return AccountResponse(
        result=False,
        addition=[account],
        description={
            "message": f"Substraction from {request.account_uuid} account is made"
        },
    )


async def read_all_status() -> AccountResponse:
    accounts = await db_query_executor.get_all()

    return AccountResponse(
        result=True, addition=accounts, description={"message": f"Get all accounts"}
    )


async def read_status(account_uuid: str) -> AccountResponse:
    account = await db_query_executor.get(account_uuid)
    raise_http_exception_on_invalid_accounts(
        account, account_uuid, validate_account_status=False
    )
    return AccountResponse(
        result=True,
        addition=[account],
        description={"message": f"Get account {account_uuid}"},
    )


async def clear_holds(delay: float) -> None:
    while True:
        logger.info("Start clearing holds")
        await db_query_executor.clear_holds()
        logger.info("Finish clearing holds")
        await asyncio.sleep(delay)


def raise_http_exception_on_invalid_accounts(
    account: AccountDBSchema,
    expected_account_uuid: str,
    validate_account_status: bool = True,
) -> None:
    if not account:
        error_message = f"Account {expected_account_uuid} was not found"
        logger.error(error_message)
        raise HTTPException(
            status_code=404,
            detail=AccountResponse(
                result=False,
                addition=[],
                description={"message": error_message},
            ).dict(),
        )

    if validate_account_status and not account.status:
        error_message = f"Account {expected_account_uuid} was already closed"
        logger.error(error_message)
        raise HTTPException(
            status_code=400,
            detail=AccountResponse(
                result=False,
                addition=[account],
                description={"message": error_message},
            ).dict(),
        )
