from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from api.v1.models import JWTRequestModel, PatchRatingModel, PostRatingModel, RatingModel
from services.ugc_service import UGCService, get_ugc_service


router = APIRouter()
ratings_tags_metadata = {
    "name": "Рейтинги",
    "description": "Управление рейтингами пользователей",
}


@router.get(
    "/",
    summary="Просмотр пользовательских рейтингов",
    description="Просмотр пользовательских рейтингов",
    response_description="Список пользовательских рейтингов",
    responses={status.HTTP_200_OK: {"model": RatingModel}},
    tags=["Рейтинги"],
)
async def get_ratings(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[RatingModel]:
    return await ugc_service.get_ratings(request.jwt_user.id, film_id)  # pyright: ignore[reportReturnType]


@router.post(
    "/{film_id}",
    summary="Добавление или изменение рейтинга",
    description="Добавление или изменение рейтинга",
    response_description="Рейтинги пользователя",
    responses={status.HTTP_201_CREATED: {"model": RatingModel}},
    tags=["Рейтинги"],
)
async def add_rating(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
    rating: Annotated[PostRatingModel, Body(description="Данные о рейтинге")],
) -> RatingModel | None:
    return await ugc_service.add_rating(request.jwt_user.id, film_id, rating.rating)  # pyright: ignore[reportReturnType]


@router.patch(
    "/{film_id}",
    summary="Изменение рейтинга",
    description="Изменение рейтинга",
    response_description="Изменённый рейтинг пользователя",
    responses={status.HTTP_200_OK: {"model": RatingModel}},
    tags=["Рейтинги"],
)
async def update_rating(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
    rating: Annotated[PatchRatingModel, Body(description="Данные о рейтинге")],
) -> RatingModel:
    if not (new_rating := await ugc_service.update_rating(request.jwt_user.id, film_id, rating.rating)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return new_rating  # pyright: ignore[reportReturnType]


@router.delete(
    "/{film_id}",
    summary="Удаление рейтинга",
    description="Удаление рейтинга",
    response_description="Подтверждение удаления рейтинга пользователя",
    responses={status.HTTP_200_OK: {}},
    tags=["Рейтинги"],
)
async def delete_rating(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
) -> None:
    await ugc_service.delete_rating(request.jwt_user.id, film_id)


@router.delete(
    "/",
    summary="Удаление всех рейтингов пользователя",
    description="Удаление всех рейтингов пользователя",
    response_description="Подтверждение удаления всех рейтингов пользователя",
    responses={status.HTTP_200_OK: {}},
    tags=["Рейтинги"],
)
async def delete_all_ratings(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
) -> None:
    await ugc_service.delete_all_ratings(request.jwt_user.id)
