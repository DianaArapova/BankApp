import asyncio

from fastapi import FastAPI, APIRouter

from app.models import accounts as account_models
from app.db import database
from app.views import ping, accounts
from app.settings import AppSettings


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(create_ping_router(), prefix="", tags=["ping"])
    app.include_router(create_account_router(), prefix="/accounts", tags=["accounts"])

    app_settings = AppSettings()
    app.router.lifespan.startup_handlers.extend(
        [
            database.connect,
            lambda: asyncio.get_running_loop().create_task(accounts.clear_holds(app_settings.clear_holds_delay))
        ]
    )
    app.router.lifespan.shutdown_handlers.append(
        [
            database.disconnect,
            asyncio.get_running_loop().stop,
        ]
    )

    return app


def create_ping_router() -> APIRouter:
    ping_router = APIRouter()
    ping_router.add_api_route(
        "/ping/",
        ping.can_we_enjoy,
        methods=["GET"],
        response_model=str
    )
    return ping_router


def create_account_router() -> APIRouter:
    account_router = APIRouter()
    routers_info = [
        ("/open/", accounts.create_account, "POST"),

        ("/status/", accounts.read_all_status, "GET"),
        ("/status/{account_uuid}/", accounts.read_status, "GET"),

        ("/close/", accounts.close_account, "PUT"),
        ("/add/", accounts.add_to_balance, "PUT"),
        ("/substract/", accounts.substract_balance, "PUT"),
    ]

    for (path, endpoint, method) in routers_info:
        account_router.add_api_route(
            path,
            endpoint,
            methods=[method],
            response_model=account_models.AccountResponse
        )

    return account_router
