from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from models.genre import Genre
from services.genre_service import GenreService, get_genre_service
from api.v1.commons import page_data
from services.validation import check_roles

router = APIRouter()


@router.get(
    '/',
    response_model=list[Genre],
    summary='Скписок всех жанров',
    description='Спиок всех жанров',
    tags=['genres'],
)
async def genre_list(
        page_data: Annotated[dict, Depends(page_data)],
        genre_service: GenreService = Depends(get_genre_service),
        check_roles: bool = Depends(check_roles),
) -> list[Genre]:
    if not check_roles:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='no role found')
    genres = await genre_service.get_all(page_data['page_size'], page_data['page_number'])
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='not found genres')
    return [Genre(id=genre.id, name=genre.name, description=genre.description) for genre in genres]


@router.get(
    '/{genre_id}',
    response_model=Genre,
    summary='Страница жанра"',
    description='Данные по конкретному жанру',
    tags=['genres'],
)
async def genre_details(
        genre_id: UUID,
        genre_service: GenreService = Depends(get_genre_service),
        check_roles: bool = Depends(check_roles),
) -> Genre:
    if not check_roles:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='no role found')
    genre = await genre_service.get_by_id(str(genre_id))
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return Genre(id=genre.id, name=genre.name, description=genre.description)
