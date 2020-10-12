from databases import Database
from starlette.testclient import TestClient

from app.models import accounts as accounts_models


def create_account(test_app: TestClient, full_name: str, start_money: int = 0) -> accounts_models.AccountDBSchema:
    open_account_request = accounts_models.OpenAccountRequest(full_name=full_name)
    response = test_app.post(
        "/accounts/open",
        data=open_account_request.json()
    )
    response_body = dict(response.json())
    account = accounts_models.AccountDBSchema(**response_body["addition"][0])

    if not start_money:
        return account

    add_request = accounts_models.ChangeAccountBalanceRequest(
        account_uuid=account.account_uuid,
        change_amount=start_money
    )
    response = test_app.put(
        "/accounts/add",
        data=add_request.json()
    )
    response_body = dict(response.json())
    account = accounts_models.AccountDBSchema(**response_body["addition"][0])

    return account


def create_closed_account(
        test_app: TestClient,
        full_name: str,
        start_money: int = 0
) -> accounts_models.AccountDBSchema:
    account = create_account(test_app, full_name, start_money)
    close_request = accounts_models.CloseAccountRequest(account_uuid=account.account_uuid)

    response = test_app.put(
        "/accounts/close",
        data=close_request.json(),
    )
    response_body = dict(response.json())
    return accounts_models.AccountDBSchema(**response_body["addition"][0])


def get_account(test_app: TestClient, account_uuid: str) -> accounts_models.AccountDBSchema:
    response = test_app.get(
        f"accounts/status/{account_uuid}"
    )
    response_body = dict(response.json())
    return accounts_models.AccountDBSchema(**response_body["addition"][0])


def test_open_account(test_app: TestClient, test_db: Database) -> None:
    full_name = "Test Account"
    open_account_request = accounts_models.OpenAccountRequest(full_name=full_name)
    response = test_app.post(
        "/accounts/open",
        data=open_account_request.json()
    )
    assert response.status_code == 200

    response_body = dict(response.json())
    account = accounts_models.AccountDBSchema(**response_body["addition"][0])

    assert response_body["result"]
    assert account.full_name == full_name


def test_get_account_by_uuid(test_app: TestClient, test_db: Database) -> None:
    accounts = [
        create_account(test_app, "First Account", 100),
        create_account(test_app, "Second Account", 200),
    ]

    for account in accounts:
        response = test_app.get(
            f"/accounts/status/{account.account_uuid}",
        )
        assert response.status_code == 200

        response_body = dict(response.json())
        assert response_body["addition"] == [account.dict()]


def test_get_all_account_by_uuid(test_app: TestClient, test_db: Database) -> None:
    accounts = [create_account(test_app, str(i), i).dict() for i in range(1, 20)]

    response = test_app.get(
        f"/accounts/status",
    )
    response_accounts = dict(response.json())["addition"]

    assert response.status_code == 200
    assert len(response_accounts) == len(accounts)
    for account in accounts:
        assert account in response_accounts


def test_close_correct_account(test_app: TestClient, test_db: Database) -> None:
    account = create_account(test_app, "Test Account")
    close_request = accounts_models.CloseAccountRequest(account_uuid=account.account_uuid)

    response = test_app.put(
        "/accounts/close",
        data=close_request.json(),
    )
    response_body = dict(response.json())

    assert response.status_code == 200
    assert response_body["result"]
    account.status = False
    assert response_body["addition"] == [account.dict()]


def test_close_closed_account(test_app: TestClient, test_db: Database) -> None:
    account = create_closed_account(test_app, "Test Account")
    close_request = accounts_models.CloseAccountRequest(account_uuid=account.account_uuid)
    response = test_app.put(
        "/accounts/close",
        data=close_request.json(),
    )
    error_detail = dict(response.json())["detail"]

    assert response.status_code == 403
    assert not error_detail["result"]


def test_add_to_correct_account(test_app: TestClient, test_db: Database) -> None:
    account = create_account(test_app, "Test Account")

    add_request = accounts_models.ChangeAccountBalanceRequest(
        account_uuid=account.account_uuid,
        change_amount=100500
    )

    response = test_app.put(
        "/accounts/add",
        data=add_request.json(),
    )
    response_body = dict(response.json())

    assert response.status_code == 200
    assert response_body["result"]
    account.balance = 100500
    assert response_body["addition"] == [account.dict()]


def test_add_to_closed_account(test_app: TestClient, test_db: Database) -> None:
    account = create_closed_account(test_app, "Test Account")

    add_request = accounts_models.ChangeAccountBalanceRequest(
        account_uuid=account.account_uuid,
        change_amount=100500
    )

    response = test_app.put(
        "/accounts/add",
        data=add_request.json(),
    )
    error_detail = dict(response.json())["detail"]

    assert response.status_code == 403
    assert not error_detail["result"]


def test_substract_from_correct_account(test_app: TestClient, test_db: Database) -> None:
    account = create_account(test_app, "Test account", start_money=100)
    money_for_substraction = 50

    substract_request = accounts_models.ChangeAccountBalanceRequest(
        account_uuid=account.account_uuid,
        change_amount=money_for_substraction,
    )

    response = test_app.put(
        "accounts/substract",
        data=substract_request.json(),
    )
    response_body = dict(response.json())

    assert response.status_code == 200
    account.holds = money_for_substraction
    assert response_body["result"]
    assert response_body["addition"] == [account.dict()]


def test_substract_from_closed_account(test_app: TestClient, test_db: Database) -> None:
    account = create_closed_account(test_app, "Test Account", 100)

    substract_request = accounts_models.ChangeAccountBalanceRequest(
        account_uuid=account.account_uuid,
        change_amount=50,
    )

    response = test_app.put(
        "accounts/substract",
        data=substract_request.json(),
    )
    error_detail = dict(response.json())["detail"]

    assert response.status_code == 403
    assert not error_detail["result"]
    assert error_detail["addition"] == [account.dict()]


def test_substract_from_account_when_there_is_not_enough_money(test_app: TestClient, test_db: Database) -> None:
    account = create_account(test_app, "Test account", start_money=100)
    money_for_substraction = 150

    substract_request = accounts_models.ChangeAccountBalanceRequest(
        account_uuid=account.account_uuid,
        change_amount=money_for_substraction,
    )

    response = test_app.put(
        "accounts/substract",
        data=substract_request.json(),
    )
    error_detail = dict(response.json())["detail"]

    assert response.status_code == 403
    assert not error_detail["result"]
    print(error_detail["addition"])
    print(account)
    assert error_detail["addition"] == [account.dict()]


def test_clear_account_holds(test_app: TestClient, test_db: Database) -> None:
    account = create_account(test_app, "Test account", start_money=100)
    money_for_substraction = 50

    substract_request = accounts_models.ChangeAccountBalanceRequest(
        account_uuid=account.account_uuid,
        change_amount=money_for_substraction,
    )

    test_app.put(
        "accounts/substract",
        data=substract_request.json(),
    )

    response = test_app.put(
        "account_testing/clear_holds"
    )

    assert response.status_code == 200
    account.balance -= money_for_substraction
    assert get_account(test_app, account.account_uuid) == account
