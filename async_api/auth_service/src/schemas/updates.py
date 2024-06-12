from pydantic import BaseModel

class RolePatch(BaseModel):
    title: str | None = None
    description: str | None = None

class UserPatch(BaseModel):
    login: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
