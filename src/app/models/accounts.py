from typing import Dict, List

from pydantic import BaseModel, conint


class OpenAccountRequest(BaseModel):
    full_name: str


class CloseAccountRequest(BaseModel):
    account_uuid: str


class ChangeAccountBalanceRequest(BaseModel):
    account_uuid: str
    change_amount: conint(gt=0)


class AccountSchema(BaseModel):
    full_name: str
    balance: int
    status: bool
    holds: int


class AccountDBSchema(AccountSchema):
    account_uuid: str


class AccountResponse(BaseModel):
    status: int = 200
    result: bool
    addition: List[AccountDBSchema]
    description: Dict[str, str]
