from enum import Enum

from pydantic import BaseModel


class AccessTokenData(BaseModel):
    iss: str
    sub: str
    iat: int
    exp: int
    roles: list[str]


class RefreshTokenData(BaseModel):
    iss: str
    sub: str
    iat: int
    exp: int