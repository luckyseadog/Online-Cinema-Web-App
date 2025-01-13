from pydantic import BaseModel


class AccessTokenData(BaseModel):
    iss: str
    sub: str
    iat: int
    exp: int
    roles: list[str]