from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status

from api.v1.models import FavouriteModel, JWTRequestModel
from services.ugc_service import UGCService, get_ugc_service


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
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[FavouriteModel]:
    return await ugc_service.get_favourites(request.jwt_user.id, film_id)  # pyright: ignore[reportReturnType]


@router.post(
    "/{film_id}",
    summary="Добавление в избранное",
    description="Добавление фильма в избранное",
    response_description="Избранное пользователя",
    responses={status.HTTP_201_CREATED: {"model": FavouriteModel}},
    tags=["Избранное"],
)
async def add_to_favourites(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
) -> FavouriteModel | None:
    return await ugc_service.add_to_favourites(request.jwt_user.id, film_id)  # pyright: ignore[reportReturnType]


@router.delete(
    "/{film_id}",
    summary="Удаление из избранного",
    description="Удаление фильма из избранного",
    response_description="Подтверждение удаления избранного пользователя",
    responses={status.HTTP_204_NO_CONTENT: {}},
    tags=["Избранное"],
)
async def remove_from_favourites(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
) -> None:
    await ugc_service.remove_from_favourites(request.jwt_user.id, film_id)


@router.delete(
    "/",
    summary="Удаление всего избранного пользователя",
    description="Удаление всего избранного пользователя",
    response_description="Подтверждение удаления всего избранного пользователя",
    responses={status.HTTP_200_OK: {}},
    tags=["Избранное"],
)
async def remove_all_favourites(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
) -> None:
    await ugc_service.remove_all_favourites(request.jwt_user.id)
