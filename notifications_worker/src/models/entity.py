from pydantic import BaseModel


class WelcomeNotification(BaseModel):
    email: str
    subject: str

    class ConfigDict:
        from_attributes = True


class NewMoviesNotification(BaseModel):
    movies: list[str]
    email: str
    subject: str

    class ConfigDict:
        from_attributes = True


class SaleNotification(BaseModel):
    email: str
    subject: str

    class ConfigDict:
        from_attributes = True
