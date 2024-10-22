from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Path, Body, Request, status

from api.v1.models import FavouriteModel, PostFavouriteModel
from services.ugc_service import UGCService, get_ugc_service


router = APIRouter()
favourites_tags_metadata = {
    "name": "Избранное",
    "description": "Управление избранным пользователя",
}


@router.get(
    "/",
    summary="Просмотр избранного",
    description="Просмотр избранного",
    response_description="Список избранного",
    responses={status.HTTP_200_OK: {"model": FavouriteModel}},
    tags=["Избранное"],
)
async def get_favourites(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    user_id: Annotated[UUID | None, Query(description="ID пользователя")] = None,
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[FavouriteModel]:
    return await ugc_service.get_favourites(user_id, film_id)


@router.post(
    "/",
    summary="Добавление в избранное",
    description="Добавление фильма в избранное",
    response_description="Избранное пользователя",
    responses={status.HTTP_201_CREATED: {"model": FavouriteModel}},
    tags=["Избранное"],
)
async def add_to_favourites(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    favourite: Annotated[PostFavouriteModel, Body(description="Данные об избранном")]
) -> FavouriteModel:
    return await ugc_service.add_to_favourites(favourite)


@router.delete(
    "/{favourite_id}",
    summary="Удаление из избранного",
    description="Удаление фильма из избранного",
    response_description="Подтверждение удаления избранного пользователя",
    responses={status.HTTP_204_NO_CONTENT: {}},
    tags=["Избранное"],
)
async def remove_from_favourites(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    favourite_id: Annotated[UUID, Path(description="ID избранного")]
) -> None:
    return await ugc_service.remove_from_favourites(favourite_id)
