from functools import wraps
from uuid import UUID

from fastapi import Depends, HTTPException, status
from src.services.token_service import get_access_token_service
from fastapi import Request


def check_token(function):
    @wraps(function)
    async def wrapper(request: Request, *args, **kwargs):
        access_token = request.cookies.get("access_token")

        access_token_service = get_access_token_service()
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access token is invalid",
            )

        if not access_token_service.validate_token(access_token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access token is invalid",
            )

        return await function(request, *args, **kwargs)

    return wrapper