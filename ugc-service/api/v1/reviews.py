from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Query, status

from api.v1.models import JWTRequestModel, PatchReviewModel, PostReviewModel, ReviewModel
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
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID | None, Query(description="ID фильма")] = None,
) -> list[ReviewModel]:
    return await ugc_service.get_reviews(request.jwt_user.id, film_id)  # pyright: ignore[reportReturnType]


@router.get(
    "/{film_id}",
    summary="Просмотр всех пользовательских рецензий на фильм",
    description="Просмотр всех пользовательских рецензий на фильм",
    response_description="Список всех пользовательских рецензий на фильм",
    responses={status.HTTP_200_OK: {"model": ReviewModel}},
    tags=["Рецензии"],
)
async def get_all_film_reviews(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
) -> list[ReviewModel]:
    return await ugc_service.get_reviews(None, film_id)  # pyright: ignore[reportReturnType]


@router.post(
    "/{film_id}",
    summary="Добавление пользовательской рецензии",
    description="Добавление пользовательской рецензии",
    response_description="Рецензии пользователя",
    responses={status.HTTP_201_CREATED: {"model": ReviewModel}},
    tags=["Рецензии"],
)
async def add_review(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
    review: Annotated[PostReviewModel, Body(description="Данные о рецензии")],
) -> ReviewModel | None:
    return await ugc_service.add_review(request.jwt_user.id, film_id, review.review)  # pyright: ignore[reportReturnType]


@router.patch(
    "/{film_id}",
    summary="Изменение рецензии",
    description="Изменение рецензии",
    response_description="Изменённая рецензия",
    responses={status.HTTP_200_OK: {"model": ReviewModel}},
    tags=["Рецензии"],
)
async def update_review(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
    review: Annotated[PatchReviewModel, Body(description="Данные о рецензии")],
) -> ReviewModel | None:
    return await ugc_service.update_review(request.jwt_user.id, film_id, review.review)  # pyright: ignore[reportReturnType]


@router.delete(
    "/{film_id}",
    summary="Удаление рецензии",
    description="Удаление рецензии",
    response_description="Рецензия удалена",
    responses={status.HTTP_200_OK: {}},
    tags=["Рецензии"],
)
async def delete_review(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
    film_id: Annotated[UUID, Path(description="ID фильма")],
) -> None:
    await ugc_service.delete_review(request.jwt_user.id, film_id)


@router.delete(
    "/",
    summary="Удаление всех рецензий пользователя",
    description="Удаление всех рецензий пользователя",
    response_description="Все рецензии пользователя удалены",
    responses={status.HTTP_200_OK: {}},
    tags=["Рецензии"],
)
async def delete_all_reviews(
    request: JWTRequestModel,
    ugc_service: Annotated[UGCService, Depends(get_ugc_service)],
) -> None:
    await ugc_service.delete_all_reviews(request.jwt_user.id)
