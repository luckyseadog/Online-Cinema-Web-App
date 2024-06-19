from typing import Annotated, Union
from uuid import uuid4

from fastapi import APIRouter, Cookie, Depends, Header, HTTPException, status
from fastapi.responses import ORJSONResponse
from fastapi.security.oauth2 import (OAuth2PasswordBearer,
                                     OAuth2PasswordRequestForm)
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from db.redis_db import RedisTokenStorage, get_redis
from schemas.entity import (AccessTokenData, History, RefreshTokenData,
                            TokenPair, User, UserCreate, UserCredentials)
from services.auth_service import auth_service
from services.history_service import history_service
from services.token_service import access_token_service, refresh_token_service
from services.user_service import user_service
from services.validation import (get_token_payload_access,
                                 get_token_payload_refresh)

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
    response: ORJSONResponse,
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
    access_token, access_exp = access_token_service.generate_token(origin, user.id, ['user'])  # TODO: add default role?
    refresh_token, refresh_exp = refresh_token_service.generate_token(origin, user.id)
    response.set_cookie(key='access_token', value=access_token, httponly=True, expires=access_exp)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, expires=refresh_exp)

    await redis.add_valid_rtoken(user.id, refresh_token)

    return {'message': 'User created successfully'}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

@router.post(
    '/login',
    # response_model=,
    status_code=status.HTTP_200_OK,
    response_model=TokenPair,
    summary='Аутентификация пользователя',
    description='''
    В теле запроса принимает два параметра: логин и пароль.
    Если пользователь аутентифицирован, вернуть его токены, если такого пользователя не
    существует или неверный пароль вернуть 401
    ''',
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: ORJSONResponse,
    origin: Annotated[str | None, Header()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
) -> TokenPair:
    if origin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Origin header is required',
        )
    user_creds = UserCredentials(login=form_data.username, password=form_data.password)
    res = await auth_service.login(user_creds, db)
    if res is True:
        user = await user_service.get_user_by_login(user_creds.login, db)
        user_roles = [role.title for role in user.roles]
        access_token, access_exp = access_token_service.generate_token(origin, user.id, user_roles)
        refresh_token, refresh_exp = refresh_token_service.generate_token(origin, user.id)
        response.set_cookie(key='access_token', value=access_token, httponly=True, expires=access_exp)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, expires=refresh_exp)

        note = History(
            user_id=user.id,
            action='/login',
            fingerprint=user_agent,
        )
        await history_service.make_note(note, db)

        await redis.add_valid_rtoken(user.id, refresh_token)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )

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
async def logout(
    response: ORJSONResponse,
    access_token: Annotated[Union[str, None], Cookie()] = None,
    refresh_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    payload: AccessTokenData = Depends(get_token_payload_access),
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    user_id = payload.sub

    note = History(
        user_id=user_id,
        action='/logout',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)

    await redis.add_banned_atoken(user_id, access_token)
    await redis.delete_refresh(user_id, refresh_token)

    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')

    return {'message': 'Success'}


@router.post(
    '/logout_all',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary='Выход пользователя из всех устройств',
    description='',
)
async def logout_all(
    response: ORJSONResponse,
    user_agent: Annotated[str | None, Header()] = None,
    payload: AccessTokenData = Depends(get_token_payload_access),
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    user_id = payload.sub

    note = History(
        user_id=user_id,
        action='/logout_all',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)

    await redis.set_user_last_logout_all(user_id)
    await redis.delete_refresh_all(user_id)

    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')

    return {'message': 'All accounts deactivated'}


@router.post(
    '/refresh',
    #     response_model=,
    status_code=status.HTTP_200_OK,
    summary='Обновление access и refresh токенов',
    description='',
)
async def refresh(
    # current_user: Annotated[User, Depends(get_current_active_user)],
    response: ORJSONResponse,
    origin: Annotated[str | None, Header()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    payload: RefreshTokenData = Depends(get_token_payload_refresh),
    db: AsyncSession = Depends(get_session),
    redis: RedisTokenStorage = Depends(get_redis),
):
    if origin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Origin header is required',
        )

    user_id = payload.sub

    note = History(
        user_id=user_id,
        action='/refresh',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)

    access_token, access_exp = access_token_service.generate_token(origin, user_id, ['user'])
    refresh_token, refresh_exp = refresh_token_service.generate_token(origin, user_id)
    response.set_cookie(key='access_token', value=access_token, httponly=True, expires=access_exp)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, expires=refresh_exp)
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
    response: ORJSONResponse,
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

    guest_create = User(
        login=f'login_{uuid4()}',
        email=f'email_{uuid4()}',
        password='',
        first_name=f'guest_{uuid4()}',
    )

    user = await user_service.create_user(guest_create, db)

    note = History(
        user_id=user.id,
        action='/signup_guest',
        fingerprint=user_agent,
    )
    await history_service.make_note(note, db)

    access_token, access_exp = access_token_service.generate_token(origin, user.id, ['guest'])
    refresh_token, refresh_exp = refresh_token_service.generate_token(origin, user.id)
    response.set_cookie(key='access_token', value=access_token, httponly=True, expires=access_exp)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, expires=refresh_exp)

    await redis.add_valid_rtoken(user.id, refresh_token)

    return {'message': 'Guest created successfully'}
