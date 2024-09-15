from pydantic import BaseModel

from test_fixtures.password import Password


class AccountModel(BaseModel):
    login: str
    password: Password | str
    first_name: str
    last_name: str
    email: str


class LoginModel(BaseModel):
    login: str
    password: str
