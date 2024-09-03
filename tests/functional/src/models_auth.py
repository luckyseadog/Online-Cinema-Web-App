from pydantic import BaseModel


class AccountModel(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str
    email: str


class LoginModel(BaseModel):
    login: str
    password: str
