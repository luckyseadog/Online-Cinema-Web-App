from models.mixins import OrjsonMixin, UUIDMixin


class Genre(UUIDMixin, OrjsonMixin):
    name: str
    description: str | None = None
