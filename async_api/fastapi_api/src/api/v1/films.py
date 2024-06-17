from http import HTTPStatus
from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from models.film import FullFilm, ShortFilm
from services.film_service import FilmService, SortModel, get_film_service
from api.v1.commons import page_data

router = APIRouter()


@router.get('/', response_model=list[ShortFilm], description='Список всех фильмов', tags=['films'])
async def get_all_films(
    page_data: Annotated[dict, Depends(page_data)],
    genre: Annotated[
        str | None, Query(
            min_length=1,
            max_length=64,
        ),
    ] = None,
    sort: Annotated[
        SortModel, Query(
            title='Sort command',
            description='Фильтры для фильмов',
        ),
    ] = SortModel('-imdb_rating'),
    film_service: FilmService = Depends(get_film_service),
):
    films = await film_service.get_all(page_data['page_size'], page_data['page_number'], genre, sort)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    films_response = [
        ShortFilm(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        ) for film in films
    ]

    return films_response


@router.get('/search', response_model=list[ShortFilm], description='Поиск фильмов', tags=['films'])
async def film_search(
    page_data: Annotated[dict, Depends(page_data)],
    query: Annotated[
        str, Query(
            title='Film name',
            description='Название фильма',
            min_length=1,
            max_length=200,
        ),
    ],
    film_service: FilmService = Depends(get_film_service),
):
    if len(query) < 1 or len(query) > 512:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Invalid query length')
    films = await film_service.search(
        query=query,
        page_size=page_data['page_size'],
        page_number=page_data['page_number'],
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    films_response = [
        ShortFilm(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        ) for film in films
    ]

    return films_response


@router.get(
    '/{film_id}',
    response_model=FullFilm,
    response_model_exclude_none=True,
    description='Фильм по id',
    tags=['films'],
)
async def film_details(film_id: UUID, film_service: FilmService = Depends(get_film_service)):
    film = await film_service.get_by_id(str(film_id))
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FullFilm(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=film.genre,
        directors=film.directors,
        actors=film.actors,
        writers=film.writers,
    )
