from models.errors import ErrorBody


class ResponseError(Exception):
    def __init__(self, response: str) -> None:
        self.response = ErrorBody(response)
        super().__init__(response)
