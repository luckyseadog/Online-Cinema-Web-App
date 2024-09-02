from pydantic import BaseModel


class ErrorBody(BaseModel):
    message: str
