from pydantic import BaseModel

class RolePatch(BaseModel):
    title: str | None = None
    description: str | None = None