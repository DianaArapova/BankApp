import json
from uuid import uuid4

from app.db_queries import accounts as accounts_db
from app.models import accounts as accounts_models


def test_open_account(test_app, monkeypatch):
    account = accounts_models.AccountDBSchema(
        account_uuid=str(uuid4()),
        full_name="Diana",
        balance=0,
        status=True,
        holds=0,
    )
    account_request = {
        "full_name": account.full_name,
    }

    async def mock_create(payload) -> str:
        return account.account_uuid

    monkeypatch.setattr(accounts_db, "create", mock_create)
    response = test_app.post(
        "/accounts/open/",
        data=json.dumps(account_request),
    )
    response_body = dict(response.json())

    assert response.status_code == 200
    assert response_body["result"]
    assert response_body["addition"] == [account.dict()]


def test_close_opened_account(test_app, monkeypatch):
    account = accounts_models.AccountDBSchema(
        account_uuid=str(uuid4()),
        full_name="Diana",
        balance=0,
        status=True,
        holds=0,
    )
    account_request = {
        "account_uuid": account.account_uuid,
    }

    async def mock_get(payload) -> accounts_db.AccountDBSchema:
        return account

    async def mock_update(payload) -> str:
        return account.account_uuid

    monkeypatch.setattr(accounts_db, "get", mock_get)
    monkeypatch.setattr(accounts_db, "update", mock_update)

    response = test_app.put(
        "/accounts/close/",
        data=json.dumps(account_request),
    )
    response_body = dict(response.json())

    assert response.status_code == 200
    assert response_body["result"]
    account.status = False
    assert response_body["addition"] == [account.dict()]


def test_():
    pass
