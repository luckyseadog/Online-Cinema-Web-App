from src.models.errors import ErrorBody


class AlreadyExistError(Exception):
    def __init__(self, response: ErrorBody) -> None:
        self.response = response
        super().__init__(response)
