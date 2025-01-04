import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    modified = models.DateTimeField(verbose_name=_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    description = models.TextField(verbose_name=_('description'), null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(verbose_name=_('full name'), max_length=255, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        SOPHOMORE = 'tv_show', _('TV Show')

    title = models.CharField(verbose_name=_('title'), max_length=255)
    description = models.TextField(verbose_name=_('description'), null=True)
    creation_date = models.DateField(verbose_name=_('creation date'), null=True)
    rating = models.FloatField(
        verbose_name=_('rating'), null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    type = models.CharField(verbose_name=_('type'), max_length=255, choices=Type.choices, null=True)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        unique_together = [['film_work', 'genre']]


class PersonFilmwork(UUIDMixin):
    class Role(models.TextChoices):
        ACTOR = 'actor', _('Actor')
        DIRECTOR = 'director', _('Director')
        WRITER = 'writer', _('Writer')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(verbose_name=_('role'), choices=Role.choices)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        unique_together = [['film_work', 'person', 'role']]
