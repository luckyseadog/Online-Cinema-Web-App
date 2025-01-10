from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Query, status

from api.v1.models import UserModel, PostRatingModel, RatingModel
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
    user_id: UUID,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[RatingModel]:
    return await ugc_service.get_ratings(user_id, film_id)  # pyright: ignore[reportReturnType]


@router.post(
    "/{film_id}",
    summary="Добавление или изменение рейтинга",
    description="Добавление или изменение рейтинга",
    response_description="Рейтинги пользователя",
    responses={status.HTTP_201_CREATED: {"model": RatingModel}},
    tags=["Рейтинги"],
)
async def add_rating(
    user: UserModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
    rating: Annotated[PostRatingModel, Body(description="Данные о рейтинге")],
) -> RatingModel | None:
    return await ugc_service.add_rating(user.id, film_id, rating.rating)  # pyright: ignore[reportReturnType]
