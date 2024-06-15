from fastapi import APIRouter
from fastapi import status, HTTPException
from services.auth_service import auth_service
from services.user_service import user_service
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from schemas.entity import UserCreate, UserCredentials, User, History
from fastapi.responses import Response
from fastapi import Header
from services.token_service import access_token_service, refresh_token_service
from db.redis_db import RedisTokenStorage, get_redis
from typing import Annotated, Union
from fastapi import Cookie
import json
import time
from uuid import uuid4
import datetime
from services.history_service import history_service


router = APIRouter()


@router.post(
    '/signup',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary='Регистрация пользователя',
    description='''
    Ручка позволяет зарегистрироваться новому пользователю\n
    В теле запроса необходимо предать:
    - login
    - password
    - first_name
    - last_name
    - email

    'Уникальными полями явлюятся: имя пользователя (login) и почта (email).
    'Если пользователь с таким логином и почтой уже существует возвращается ошибка 409 с описанием,
    'что такой пользователь уже существует.\n''
    ''',
)
async def signup(
    user_create: UserCreate,
    response: Response,
    origin: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    if origin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Origin header is required',
        )
    user = await user_service.get_user_by_email(user_create.email, db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='email already exists')
    user = await user_service.get_user_by_login(user_create.login, db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='login already exists')

    user = await user_service.create_user(user_create, db)
    access_token = access_token_service.generate_token(origin, str(user.id), ['user'])  # TODO: add default role?
    refresh_token = refresh_token_service.generate_token(origin, str(user.id))
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

    # await redis.add_valid_rtoken(user.id, refresh_token)

    return {'message': 'User created successfully'}


@router.post(
    '/login',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary='Аутентификация пользователя',
    description='''
    В теле запроса принимает два параметра: логин и пароль.
    Если пользователь аутентифицирован, вернуть его токены, если такого пользователя не
    существует или неверный пароль вернуть 401
    ''',
)
async def login(
    user_creds: UserCredentials,
    response: Response,
    origin: Annotated[str | None, Header()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    if origin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Origin header is required',
        )
    res = await auth_service.login(user_creds, db)
    if res is True:
        user = await user_service.get_user_by_login(user_creds.login)
        access_token = access_token_service.generate_token(origin, user.id, ['user'])  # TODO: add default role?
        refresh_token = refresh_token_service.generate_token(origin, user.id)
        response.set_cookie(key='access_token', value=access_token, httponly=True)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

        note = History(
            user_id=user.id,
            occured_at=datetime.datetime.now(),
            action='/login',
            fingerprint=user_agent,
        )
        await history_service.make_note(note)

        await redis.add_valid_rtoken(user.id, refresh_token)

        return {'message': 'Success'}

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Login error',  # TODO: which error?
        )

@router.post(
    '/logout',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary='Выход пользователя',
    description='Из токена получается id пользователя. '
                'Токен помещается в кеш забаненнных access токенов. '
                'Если пользователь решит снова аутентифицироваться, то ему придётся ввести логин и пароль.',
)
# async def logout(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user
async def logout(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    redis: RedisTokenStorage = Depends(get_redis),
):
    if access_token is None and refresh_token is None:
        return {'message': 'You are not logged in'}

    if not access_token_service.validate_token(access_token):
        return {'message': 'Invalid access token'}
    elif await redis.check_banned_atoken(access_token) is True:
        return {'message': 'Invalid access token'}

    payload_str = access_token_service.decode_b64(access_token).split('.')[1]
    payload = json.loads(payload_str)

    if payload['exp'] < time.time():
        return {'message': 'Invalid access token'}

    user_id = payload.get('sub')

    note = History(
        user_id=user_id,
        occured_at=datetime.datetime.now(),
        action='/logout',
        fingerprint=user_agent,
    )
    await history_service.make_note(note)

    await redis.add_banned_atoken(user_id, access_token)
    await redis.delete_refresh(user_id, refresh_token)

    return {'message': 'Success'}


@router.post(
    '/logout_all',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary='Выход пользователя из всех устройств',
    description='',
)
async def logout_all(
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    redis: RedisTokenStorage = Depends(get_redis),
):
    if access_token is None:
        return {'message': 'You are not logged in'}

    if not access_token_service.validate_token(access_token):
        return {'message': 'Invalid access token'}
    elif await redis.check_banned_atoken(access_token) is True:
        return {'message': 'Invalid access token'}

    payload_str = access_token_service.decode_b64(access_token).split('.')[1]
    payload = json.loads(payload_str)

    if payload['exp'] < time.time():
        return {'message': 'Invalid access token'}

    user_id = payload.get('sub')

    note = History(
        user_id=user_id,
        occured_at=datetime.datetime.now(),
        action='/logout_all',
        fingerprint=user_agent,
    )
    await history_service.make_note(note)

    await redis.set_user_last_logout_all(user_id)
    await redis.delete_refresh_all(user_id)

    return {'message': 'logout_all'}


@router.post(
    '/refresh',
    #     response_model=,
    status_code=status.HTTP_200_OK,
    summary='Обновление access и refresh токенов',
    description='',
)
async def refresh(
    response: Response,
    origin: Annotated[str | None, Header()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    redis: RedisTokenStorage = Depends(get_redis),
):
    if origin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Origin header is required',
        )

    if refresh_token is None:
        return {'message': 'Invalid refresh is required'}

    if not refresh_token_service.validate_token(refresh_token):
        return {'message': 'Invalid refresh token'}
    # elif await redis.check_valid_rtoken(refresh_token) == False:
    #     return {"message": "Invalid refresh token"}

    payload_str = refresh_token_service.decode_b64(refresh_token).split('.')[1]
    payload = json.loads(payload_str)

    if payload['exp'] < time.time():
        return {'message': 'Invalid refresh token'}

    user_id = payload.get('sub')

    note = History(
        user_id=user_id,
        occured_at=datetime.datetime.now(),
        action='/refresh',
        fingerprint=user_agent,
    )
    await history_service.make_note(note)

    access_token = access_token_service.generate_token(origin, user_id, ['user'])  # TODO: add default role?
    refresh_token = refresh_token_service.generate_token(origin, user_id)
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

    await redis.add_valid_rtoken(user_id, refresh_token)

    return {'message': 'Success'}

@router.post(
    '/signup_guest',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary='Регистрация гостевого пользователя',
    description='''
    В теле запроса принимает два параметра: логин и пароль.
    - Если пользователь с таким логином уже существует возвращается ошибка 409 с
    описанием что такой пользователь уже существует.\n
    - Если пользователь с таким логином не существует, то он добавляется.\
    ''',
)
async def signup_guest(
    response: Response,
    origin: Annotated[str | None, Header()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    if origin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Origin header is required',
        )

    guest_create = User(login='', passwod='', first_name=f'guest_{uuid4()}')

    user = await user_service.create_user(guest_create, db)

    note = History(
        user_id=user.id,
        occured_at=datetime.datetime.now(),
        action='/signup_guest',
        fingerprint=user_agent,
    )
    await history_service.make_note(note)

    access_token = access_token_service.generate_token(origin, user.id, ['guest'])  # TODO: add default role?
    refresh_token = refresh_token_service.generate_token(origin, user.id)
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

    await redis.add_valid_rtoken(user.id, refresh_token)

    return {'message': 'Guest created successfully'}
