import asyncio

import pytest
from databases import Database
from fastapi import APIRouter
from starlette.testclient import TestClient


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    from app.app_entrypoint import create_app

    app = create_app()
    app.include_router(
        create_router_for_testing(), prefix="/account_testing", tags=["account_testing"]
    )

    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
@pytest.mark.asyncio
async def test_db(test_app: TestClient, event_loop) -> Database:
    from sqlalchemy import create_engine

    from app.db import database, metadata
    from app.settings import DBSettings

    db_settings = DBSettings()
    print(db_settings)
    await database.connect()

    engine = create_engine(db_settings.url)
    metadata.bind = engine
    metadata.create_all()

    yield database

    metadata.drop_all()
    await database.disconnect()


def create_router_for_testing() -> APIRouter:
    import app.models.accounts as account_models
    from app.views import accounts

    router_for_testing = APIRouter()

    router_for_testing.add_api_route(
        "/clear_holds",
        accounts.clear_holds_once,
        methods=["PUT"],
        response_model=account_models.AccountResponse,
    )

    return router_for_testing
