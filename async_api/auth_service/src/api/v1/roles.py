from fastapi import status
from db.postgres import AsyncSession, get_session
from fastapi import APIRouter, Depends
from schemas.entity import Role
from services.role_service import role_service
from db.redis_db import RedisTokenStorage, get_redis
from uuid import UUID


router = APIRouter()


@router.get(
    '/roles',
    response_model=list[Role],
    status_code=status.HTTP_200_OK,
    summary='Получение списка ролей',
    description='',
)
async def get_roles(
    # access_token: Annotated[Union[str, None], Cookie()] = None,
    # refresh_token: Annotated[Union[str, None], Cookie()] = None,
    # user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    # redis: RedisTokenStorage = Depends(get_redis),
) -> list[Role]:

    # try:
    #     payload = await validate_token(access_token, refresh_token, redis)
    # except AuthError as e:
    #     raise HTTPException(status_code=401, detail=e.message)
    #
    # note = History(user_id=payload["sub"],
    #                occured_at=datetime.datetime.now(),
    #                action="/roles[GET]",
    #                fingerprint=user_agent)
    # await history_service.make_note(note)
    return await role_service.get_roles(db)


@router.post(
    '/roles',
    response_model=Role,
    status_code=status.HTTP_200_OK,
    summary='Добавление роли',
    description='',
)
async def add_role(
    role_create: Role,
    # access_token: Annotated[Union[str, None], Cookie()] = None,
    # refresh_token: Annotated[Union[str, None], Cookie()] = None,
    # user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    # redis: RedisTokenStorage = Depends(get_redis),
):
    # try:
    #     payload = await validate_token(access_token, refresh_token, redis)
    # except AuthError as e:
    #     raise HTTPException(status_code=401, detail=e.message)
    #
    # note = History(user_id=payload["sub"],
    #                occured_at=datetime.datetime.now(),
    #                action="/roles[post]",
    #                fingerprint=user_agent)
    # await history_service.make_note(note)
    return await role_service.create_role(db=db, role_create=role_create)


@router.put(
    '/roles',
    #     response_model=,
    status_code=status.HTTP_200_OK,
    summary='Обновление роли',
    description='',
)
async def update_role(
    role_create: Role,
    # access_token: Annotated[Union[str, None], Cookie()] = None,
    # refresh_token: Annotated[Union[str, None], Cookie()] = None,
    # user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    # try:
    #     payload = await validate_token(access_token, refresh_token, redis)
    # except AuthError as e:
    #     raise HTTPException(status_code=401, detail=e.message)
    #
    # note = History(user_id=payload["sub"],
    #                occured_at=datetime.datetime.now(),
    #                action="/roles[put]",
    #                fingerprint=user_agent)
    # await history_service.make_note(note)
    return await role_service.update_role(role_create, db)


@router.delete(
    '/roles',
    status_code=status.HTTP_200_OK,
    summary='Удаление роли',
    description='',
)
async def delete_role(
    id: UUID,
    # access_token: Annotated[Union[str, None], Cookie()] = None,
    # refresh_token: Annotated[Union[str, None], Cookie()] = None,
    # user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    # redis: RedisTokenStorage = Depends(get_redis),
):
    # try:
    #     payload = await validate_token(access_token, refresh_token, redis)
    # except AuthError as e:
    #     raise HTTPException(status_code=401, detail=e.message)
    #
    # note = History(user_id=payload["sub"],
    #                occured_at=datetime.datetime.now(),
    #                action="/roles[delete]",
    #                fingerprint=user_agent)
    # await history_service.make_note(note)
    return await role_service.delete_role(id, db)
