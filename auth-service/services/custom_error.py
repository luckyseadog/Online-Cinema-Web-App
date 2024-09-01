from models.errors import ErrorBody


class ResponseError(Exception):
    def __init__(self, response: ErrorBody) -> None:
        self.response = response
        super().__init__(response)
