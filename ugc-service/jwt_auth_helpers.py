from collections.abc import Callable, Collection, Coroutine
from functools import wraps
from typing import Annotated, Any, ParamSpec, TypeVar
from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer

from api.v1.models import JWTUserModel
from services.redis_service import RedisService, get_redis_service


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def rights_required(
    required_rights_names_list: Collection[str],
) -> Callable[[Callable[F_Spec, F_Return]], Callable[F_Spec, Coroutine[Any, Any, F_Return]]]:
    def decorator(function: Callable[F_Spec, Any]) -> Callable[F_Spec, Coroutine[Any, Any, F_Return]]:
        @wraps(function)
        async def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            # Доствём ранее положенные данные из запроса
            user: JWTUserModel = kwargs.get("request").jwt_user
            # Проверяем, что текущий пользователь имеет все требуемые права
            if not user or any(right not in user.rights for right in required_rights_names_list):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

            return await function(*args, **kwargs)

        return wrapper

    return decorator


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False) -> None:
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
        redis_service: Annotated[RedisService, Depends(get_redis_service)],
    ) -> JWTUserModel:
        authorize = AuthJWT(req=request)
        # Достаём Access Token и проверяем его на коректность
        await authorize.jwt_optional()
        # Получаем идентификатор текущего пользователя из Access Token'а
        user_id = await authorize.get_jwt_subject()
        # Проверяем, токен на logout
        if not user_id or await redis_service.check_banned_access(user_id, authorize._token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        # Получаем права текущего пользователя из Redis'а
        user_rights = await redis_service.get_user_rights(UUID(user_id))
        all_rights = await redis_service.get_all_rights()
        user_rights = [right[1] for right in all_rights if right[0] in user_rights]
        # Возвращаем модель JWT пользователя с его ID и правами
        return JWTUserModel(id=user_id, rights=user_rights)


async def get_jwt_user_global(request: Request, user: Annotated[JWTUserModel, Depends(JWTBearer())]) -> None:
    # Кладём в request пользователя токена с его правами
    request.jwt_user = user
