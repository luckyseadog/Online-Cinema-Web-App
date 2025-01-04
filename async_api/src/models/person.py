from models.mixins import OrjsonMixin, UUIDMixin


class Person(UUIDMixin, OrjsonMixin):
    name: str


class FilmsByPerson(UUIDMixin, OrjsonMixin):
    roles: list[str] | None = []


class PersonFilmsRoles(Person, OrjsonMixin):
    films: list[FilmsByPerson]
