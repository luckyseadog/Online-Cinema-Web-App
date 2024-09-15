import uuid
from typing import Annotated

import aiohttp
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from api.v1.models import AccountModel, ActualTokensModel, HistoryModel
from core.config import JWTConfig, jwt_config, oauth_config
from models.alchemy_model import Action
from services.redis_service import RedisService, get_redis
from services.user_service import UserService, get_user_service


router = APIRouter()
auth_dep = AuthJWTBearer()


@AuthJWT.load_config
def get_config() -> JWTConfig:
    return jwt_config


@router.get(
    "/go/oauth2callback",
    status_code=status.HTTP_200_OK,
)
async def google_oauth(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)],
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    code: str | None = None,
    state: str | None = None,
):
    if not code:  # if we dont have google access token in Redis
        auth_uri = (
            f"https://accounts.google.com/o/oauth2/v2/auth?scope={oauth_config.google_scope}&"
            "access_type=offline&response_type=code&"
            f"state={oauth_config.google_state}&client_id={oauth_config.google_client_id}&redirect_uri={oauth_config.google_redirect_uri}"
        )
        return RedirectResponse(auth_uri, status_code=302)
    else:
        if not state:
            raise HTTPException(status_code=400, detail="no state")
        data = {
            "code": code,
            "client_id": oauth_config.google_client_id,
            "client_secret": oauth_config.google_client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": oauth_config.google_redirect_uri,
        }
        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            async with session.post("https://oauth2.googleapis.com/token", data=data, headers=headers) as resp:
                tokens = await resp.json()

            access_token = tokens.get("access_token")
            if not access_token:
                raise HTTPException(status_code=500, detail=tokens)

            headers = {"Authorization": f"Bearer {access_token}"}
            async with session.get("https://www.googleapis.com/oauth2/v2/userinfo?alt=json", headers=headers) as resp:
                user_data = await resp.json()

        user = await user_service.get_user(user_data.get("email"))
        if not user:
            new_user_model = AccountModel(
                login=user_data["email"],
                first_name=user_data["given_name"],
                last_name=user_data["family_name"],
                email=user_data["email"],
                password=str(uuid.uuid4()),
            )
            user = await user_service.create_user(new_user_model)

        access_token = await authorize.create_access_token(subject=str(user.id))
        refresh_token = await authorize.create_refresh_token(subject=access_token)

        user_right_ids = [right.id for right in user.rights]
        await redis.add_valid_refresh(user.id, refresh_token, access_token)
        await redis.add_user_right(user.id, user_right_ids)

        await user_service.save_history(
            HistoryModel(
                user_id=user.id,
                ip_address=request.client.host if request.client else "",
                action=Action.LOGIN,
                browser_info=request.headers.get("user-agent", ""),
                system_info=request.headers.get("sec-ch-ua-platform", ""),
            )
        )

        await authorize.set_access_cookies(access_token)
        await authorize.set_refresh_cookies(refresh_token)
        return ActualTokensModel(access_token=access_token, refresh_token=refresh_token)


@router.get(
    "/ya/oauth2callback",
    status_code=status.HTTP_200_OK,
)
async def yandex_oauth(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)],
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    code: str | None = None,
    state: str | None = None,
):
    if not code:  # if we dont have google access token in Redis
        auth_uri = (
            f"https://oauth.yandex.ru/authorize?scope={oauth_config.yandex_scope}&"
            f"response_type=code&state={oauth_config.yandex_state}&client_id={oauth_config.yandex_client_id}&redirect_uri={oauth_config.yandex_redirect_uri}"
        )
        return RedirectResponse(auth_uri, status_code=302)
    else:
        if not state:
            raise HTTPException(status_code=400, detail="no state")
        data = {
            "code": code,
            "client_id": oauth_config.yandex_client_id,
            "client_secret": oauth_config.yandex_client_secret,
            "grant_type": "authorization_code",
        }
        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            async with session.post("https://oauth.yandex.ru/token", data=data, headers=headers) as resp:
                tokens = await resp.json()

            access_token = tokens.get("access_token")
            if not access_token:
                raise HTTPException(status_code=500, detail=tokens)

            headers = {"Authorization": f"Bearer {access_token}"}
            async with session.get("https://login.yandex.ru/info?alt=json", headers=headers) as resp:
                user_data = await resp.json()

        user = await user_service.get_user(user_data.get("default_email"))
        if not user:
            new_user_model = AccountModel(
                login=user_data["default_email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["default_email"],
                password=str(uuid.uuid4()),
            )
            user = await user_service.create_user(new_user_model)

        access_token = await authorize.create_access_token(subject=str(user.id))
        refresh_token = await authorize.create_refresh_token(subject=access_token)

        user_right_ids = [right.id for right in user.rights]
        await redis.add_valid_refresh(user.id, refresh_token, access_token)
        await redis.add_user_right(user.id, user_right_ids)

        await user_service.save_history(
            HistoryModel(
                user_id=user.id,
                ip_address=request.client.host if request.client else "",
                action=Action.LOGIN,
                browser_info=request.headers.get("user-agent", ""),
                system_info=request.headers.get("sec-ch-ua-platform", ""),
            )
        )

        await authorize.set_access_cookies(access_token)
        await authorize.set_refresh_cookies(refresh_token)
        return ActualTokensModel(access_token=access_token, refresh_token=refresh_token)
