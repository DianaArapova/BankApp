import json
from uuid import uuid4

from app.db_queries import accounts as accounts_db


def test_create_account(test_app, monkeypatch):
    account_request = {
        "full_name": "diana",
    }
    account_uuid = str(uuid4())

    async def mock_create(payload):
        return account_uuid

    monkeypatch.setattr(accounts_db, "create", mock_create)
    response = test_app.post("/accounts/", data=json.dumps(account_request),)
    response_body = dict(response.json())

    assert response.status_code == 201
    assert response_body["result"]
    assert response_body["addition"] == {
        "account_uuid": account_uuid,
        "full_name": "diana",
        "balance": 0,
        "holds": 0,
        "status": True
    }


def test_close_account(test_app, monkeypatch):
    pass
