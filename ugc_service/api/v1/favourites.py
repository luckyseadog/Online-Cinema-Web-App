from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status

from api.v1.models import FavouriteModel, UserModel
from services.ugc_service import UGCService, get_ugc_service
from uuid import UUID


router = APIRouter()
favourites_tags_metadata = {"name": "Избранное", "description": "Управление избранным пользователя"}


@router.get(
    "/",
    summary="Просмотр избранного",
    description="Просмотр избранного",
    response_description="Список избранного",
    responses={status.HTTP_200_OK: {"model": FavouriteModel}},
    tags=["Избранное"],
)
async def get_favourites(
    user_id: UUID,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[FavouriteModel]:
    return await ugc_service.get_favourites(user_id, film_id)  # pyright: ignore[reportReturnType]


@router.post(
    "/{film_id}",
    summary="Добавление в избранное",
    description="Добавление фильма в избранное",
    response_description="Избранное пользователя",
    responses={status.HTTP_201_CREATED: {"model": FavouriteModel}},
    tags=["Избранное"],
)
async def add_to_favourites(
    user: UserModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
) -> FavouriteModel | None:
    return await ugc_service.add_to_favourites(user.id, film_id)  # pyright: ignore[reportReturnType]


@router.delete(
    "/{film_id}",
    summary="Удаление из избранного",
    description="Удаление фильма из избранного",
    response_description="Подтверждение удаления избранного пользователя",
    responses={status.HTTP_204_NO_CONTENT: {}},
    tags=["Избранное"],
)
async def remove_from_favourites(
    user: UserModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
) -> None:
    await ugc_service.remove_from_favourites(user.id, film_id)