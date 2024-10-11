from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from api.v1.models import FavouriteModel, RatingModel, ReviewModel
from services.ugc_service import UGCService, get_ugc_service


router = APIRouter()
ugc_tags_metadata = {
    "name": "Пользовательский контент",
    "description": "Получение информации по пользовательскому контенту",
}


@router.get(
    "/ratings",
    summary="Просмотр пользовательских рейтингов",
    description="Просмотр пользовательских рейтингов",
    response_description="Список пользовательских рейтингов",
    responses={status.HTTP_200_OK: {"model": RatingModel}},
    tags=["Пользовательский контент"],
)
async def get_ratings(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    user_id: Annotated[UUID | None, Query(description="ID пользолвателя")] = None,
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[RatingModel]:
    return await ugc_service.get_ratings(user_id, film_id)


@router.get(
    "/reviews",
    summary="Просмотр пользовательских обзоров",
    description="Просмотр пользовательских обзоров",
    response_description="Список пользовательских обзоров",
    responses={status.HTTP_200_OK: {"model": ReviewModel}},
    tags=["Пользовательский контент"],
)
async def get_reviews(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    user_id: Annotated[UUID | None, Query(description="ID пользолвателя")] = None,
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[ReviewModel]:
    return await ugc_service.get_reviews(user_id, film_id)


@router.get(
    "/favourites",
    summary="Просмотр избранного",
    description="Просмотр избранного",
    response_description="Список избранного",
    responses={status.HTTP_200_OK: {"model": FavouriteModel}},
    tags=["Пользовательский контент"],
)
async def get_favourites(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    user_id: Annotated[UUID | None, Query(description="ID пользолвателя")] = None,
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[FavouriteModel]:
    return await ugc_service.get_favourites(user_id, film_id)
