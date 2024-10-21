from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Path, Body, Request, status

from api.v1.models import ReviewModel, PostReviewModel, PatchReviewModel
from services.ugc_service import UGCService, get_ugc_service


router = APIRouter()
reviews_tags_metadata = {
    "name": "Рецензии",
    "description": "Управление рецензиями пользователей",
}


@router.get(
    "/",
    summary="Просмотр пользовательских рецензий",
    description="Просмотр пользовательских рецензий",
    response_description="Список пользовательских рецензий",
    responses={status.HTTP_200_OK: {"model": ReviewModel}},
    tags=["Рецензии"],
)
async def get_reviews(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    user_id: Annotated[UUID | None, Query(description="ID пользователя")] = None,
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[ReviewModel]:
    return await ugc_service.get_reviews(user_id, film_id)


@router.post(
    "/",
    summary="Добавление пользовательской рецензии",
    description="Добавление пользовательской рецензии",
    response_description="Рецензии пользователя",
    responses={status.HTTP_201_CREATED: {"model": ReviewModel}},
    tags=["Рецензии"],
)
async def add_review(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    review: Annotated[PostReviewModel, Body(description="Данные о рецензии")],
) -> ReviewModel:
    return await ugc_service.add_review(review)


@router.patch(
    "/{review_id}",
    summary="Изменение рецензии",
    description="Изменение рецензии",
    response_description="Изменённая рецензия",
    responses={status.HTTP_200_OK: {"model": ReviewModel}},
    tags=["Рецензии"],
)
async def update_review(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    review_id: Annotated[UUID, Path(description="ID рецензии")],
    review: Annotated[PatchReviewModel, Body(description="Данные о рецензии")],
) -> ReviewModel:
    return await ugc_service.update_review(review_id, review)


@router.delete(
    "/{review_id}",
    summary="Удаление рецензии",
    description="Удаление рецензии",
    response_description="Рецензия удалена",
    responses={status.HTTP_204_NO_CONTENT: {}},
    tags=["Рецензии"],
)
async def delete_review(
    request: Request,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    review_id: Annotated[UUID, Path(description="ID рецензии")],
) -> None:
    return await ugc_service.delete_review(review_id)
