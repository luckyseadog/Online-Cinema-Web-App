from collections.abc import Callable, Collection, Coroutine
from functools import wraps
from typing import Annotated, Any, ParamSpec, TypeVar, cast
from uuid import UUID

from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer

from api.v1.models import JWTUserModel, RightsModel
from services.redis_service import RedisService, get_redis
from services.rights_management_service import RightsManagementService, get_rights_management_service


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def rights_required(
    required_rights_names_list: Collection[str],
) -> Callable[[Callable[F_Spec, F_Return]], Callable[F_Spec, Coroutine[Any, Any, F_Return]]]:
    def decorator(function: Callable[F_Spec, Any]) -> Callable[F_Spec, Coroutine[Any, Any, F_Return]]:
        @wraps(function)
        async def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            # Достaём ранее положенные данные из запроса
            user = cast(JWTUserModel | None, kwargs.get("request").jwt_user)
            all_rights = cast(RightsModel, kwargs.get("request").all_rights)
            # Собираем UUIDы требуемых прав по названиям
            required_rights_uuids = {
                right.id for right in all_rights.rights if right.name in required_rights_names_list
            }
            # Проверяем, что текущий пользователь имеет все требуемые права
            if (
                not user
                or not required_rights_uuids
                or any(right not in user.rights for right in required_rights_uuids)
            ):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

            return await function(*args, **kwargs)

        return wrapper

    return decorator


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False) -> None:
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request, redis_service: Annotated[RedisService, Depends(get_redis)]
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
        rights = await redis_service.get_user_rights(UUID(user_id))
        # Возвращаем модель JWT пользователя с его ID и правами
        return JWTUserModel(id=user_id, rights=rights)


async def get_all_rights(
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
) -> RightsModel:
    # Кладём все права из базы в request для дальнейших проверок
    # Это делается так для упрощения взаимоедействия сервисом прав через функционал Depends FastAPi
    return await rights_management_service.get_all()


async def get_jwt_user_global(
    request: Request,
    user: Annotated[JWTUserModel, Depends(JWTBearer())],
    all_rights: Annotated[RightsModel, Depends(get_all_rights)],
) -> None:
    # Кладём в request все права и пользователя токена с его правами
    request.all_rights = all_rights
    request.jwt_user = user
