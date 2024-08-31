from pydantic import BaseModel


class ErrorBody(BaseModel):
    massage: str
