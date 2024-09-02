from models.errors import ErrorBody


class ResponseError(Exception):
    def __init__(self, message: str) -> None:
        self.message = ErrorBody(message=message)
