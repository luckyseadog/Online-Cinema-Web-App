from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from models.film import ShortFilm
from models.person import Person, PersonFilmsRoles
from services.person_service import PersonService, get_person_service
from api.v1.commons import page_data

router = APIRouter()


@router.get(
    '/',
    summary='Список всех персон"',
    description='Спиок всех персон',
    response_model=list[Person],
)
async def person_all(
        page_data: Annotated[dict, Depends(page_data)],
        person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    persons = await person_service.get_all(page_data["page_size"], page_data["page_number"])
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='not found persons')
    return [Person(id=person.id, name=person.name) for person in persons]


@router.get(
    '/search',
    response_model=list[PersonFilmsRoles],
    summary='Поиск по персонам"',
    description='Полнотекстовый поиск по персонам',
    tags=['persons'],
)
async def person_search(
        page_data: Annotated[dict, Depends(page_data)],
        query: Annotated[
            str, Query(
                title='Person name',
                description='Имя персонажа',
                min_length=3,
                max_length=50,
            ),
        ],
        person_service: PersonService = Depends(get_person_service),
) -> list[PersonFilmsRoles]:
    persons = await person_service.search(query, page_data["page_size"], page_data["page_number"])
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'not found persons by key: {query}')
    return [PersonFilmsRoles(id=person.id, name=person.name, films=person.films) for person in persons]


@router.get(
    '/{person_id}',
    response_model=PersonFilmsRoles,
    summary='Данные по персонажа"',
    description='Информация о персоне и её фильмография',
    tags=['persons'],
)
async def person_deatils(
        person_id: UUID,
        person_service: PersonService = Depends(get_person_service),
) -> PersonFilmsRoles:
    person = await person_service.get_by_id(str(person_id))
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonFilmsRoles(id=person.id, name=person.name, films=person.films)


@router.get(
    '/{person_id}/films',
    response_model=list[ShortFilm],
    summary='Страница персонажа с его фильмотекой',
    description='Страница персонажа с его фильмотекой',
    response_description='Информацияо персоне и её фильмография',
    tags=['persons'],
)
async def person_films(
        person_id: UUID,
        person_service: PersonService = Depends(get_person_service),
) -> list[ShortFilm]:
    films = await person_service.get_person_films(str(person_id))
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person films not found')
    return [ShortFilm(id=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]
