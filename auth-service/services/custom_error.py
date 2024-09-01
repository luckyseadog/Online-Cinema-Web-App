from models.errors import ErrorBody


class ResponseError(Exception):
    def __init__(self, massage: str) -> None:
        self.massage = ErrorBody(massage=massage)
        super().__init__(massage)
