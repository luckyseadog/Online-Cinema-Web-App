from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Query, Request, status

from api.v1.models import PatchRatingModel, PostRatingModel, RatingModel
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
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    user_id: Annotated[UUID | None, Query(description="ID пользователя")] = None,
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[RatingModel]:
    return await ugc_service.get_ratings(user_id, film_id)  # pyright: ignore[reportReturnType]


@router.post(
    "/",
    summary="Добавление или изменение рейтинга",
    description="Добавление или изменение рейтинга",
    response_description="Рейтинги пользователя",
    responses={status.HTTP_201_CREATED: {"model": RatingModel}},
    tags=["Рейтинги"],
)
async def add_rating(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    rating: Annotated[PostRatingModel, Body(description="Данные о рейтинге")],
) -> RatingModel | None:
    return await ugc_service.add_rating(rating)  # pyright: ignore[reportReturnType]


@router.patch(
    "/{rating_id}",
    summary="Изменение рейтинга",
    description="Изменение рейтинга",
    response_description="Изменённый рейтинг пользователя",
    responses={status.HTTP_200_OK: {"model": RatingModel}},
    tags=["Рейтинги"],
)
async def update_rating(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    rating_id: Annotated[UUID, Path(description="ID рейтинга")],
    rating: Annotated[PatchRatingModel, Body(description="Данные о рейтинге")],
) -> RatingModel:
    return await ugc_service.update_rating(rating_id, rating)  # pyright: ignore[reportReturnType]


@router.delete(
    "/{rating_id}",
    summary="Удаление рейтинга",
    description="Удаление рейтинга",
    response_description="Подтверждение удаления рейтинга пользователя",
    responses={status.HTTP_204_NO_CONTENT: {}},
    tags=["Рейтинги"],
)
async def delete_rating(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    rating_id: Annotated[UUID, Path(description="ID рейтинга")],
) -> None:
    return await ugc_service.delete_rating(rating_id)
