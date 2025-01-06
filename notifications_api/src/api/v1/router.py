import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from src.models.entity import User
from src.services.movies_service import MovieService, get_movie_service
from src.services.notification_service import (
    NotificationService,
    get_notification_service,
)
from src.services.rate_limiter_service import TokenBucket, get_token_bucket
from src.helpers.rights import check_token
from fastapi import Request

router = APIRouter(prefix="/notifications")


@router.post('/greeting', status_code=status.HTTP_202_ACCEPTED)
async def send_greeting_notification(
    request: Request, 
    users: list[User], 
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    token_bucket_service: Annotated[TokenBucket, Depends(get_token_bucket)],
):
    emails = []
    for user in users:
        if await token_bucket_service.request_permisson(user.id):
            emails.append(user.email)
        else:
            logging.debug(f"{user.id}: limit of notifications exceeded")
    try:
        logging.debug(f"EMALS: {emails}")
        notification_service.send_welcome_event("welcome.txt", emails)
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/new_movies', status_code=status.HTTP_202_ACCEPTED)
@check_token
async def send_new_movies_notification(
    request: Request, 
    users: list[User],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    token_bucket_service: Annotated[TokenBucket, Depends(get_token_bucket)],
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
):
    emails = []
    for user in users:
        if await token_bucket_service.request_permisson(user.id):
            emails.append(user.email)
        else:
            logging.debug(f"{user.id}: limit of notifications exceeded")
    movies_names = await movie_service.get_new_movies()
    try:
        notification_service.send_new_movies_event("new_movies.txt", emails, movies_names)
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/sale_event', status_code=status.HTTP_202_ACCEPTED)
@check_token
async def send_greeting_notification(
    request: Request, 
    users: list[User], 
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    token_bucket_service: Annotated[TokenBucket, Depends(get_token_bucket)],
):
    emails = []
    for user in users:
        if await token_bucket_service.request_permisson(user.id):
            emails.append(user.email)
        else:
            logging.debug(f"{user.id}: limit of notifications exceeded")
    try:
        notification_service.send_sale_event("sale.txt", emails)
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
