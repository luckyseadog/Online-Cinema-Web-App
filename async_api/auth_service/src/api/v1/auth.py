from typing import Annotated, Union

from fastapi import APIRouter, Cookie, Depends, Header, HTTPException, status
from fastapi.responses import ORJSONResponse
from fastapi.security.oauth2 import (
    OAuth2PasswordRequestForm,
)

from core.config import settings
from schemas.entity_schemas import (
    AccessTokenData, RefreshTokenData,
    TokenPair, UserCreate, UserCredentials,
)

from services.user_service import UserService, get_user_service
from services.auth_service import AuthService, get_auth_service
from services.validation import validate_access_token, validate_refresh_token

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
    user_service: Annotated[UserService, Depends(get_user_service)],
    response: ORJSONResponse,
    origin: Annotated[str | None, Header()] = None,
):

    if origin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Origin header is required',
        )
    user = await user_service.get_user_by_email(user_create.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='email already exists')

    user = await user_service.get_user_by_login(user_create.login)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='login already exists')

    user = await user_service.create_user(user_create)
    # access_token, access_exp = access_token_service.generate_token(origin, user.id, ['user'])
    # TODO: add default role?
    # refresh_token, refresh_exp = refresh_token_service.generate_token(origin, user.id)
    # response.set_cookie(key=settings.access_token_name, value=access_token, httponly=True, expires=access_exp)
    # response.set_cookie(key=settings.refresh_token_name, value=refresh_token, httponly=True, expires=refresh_exp)
#    await redis.add_valid_rtoken(user.id, refresh_token)
    return {'message': 'User created successfully'}


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
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    response: ORJSONResponse,
    origin: Annotated[str | None, Header()] = None,
    user_agent: Annotated[str | None, Header()] = None,
) -> TokenPair:
    if origin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Origin header is required',
        )
    user_creds = UserCredentials(login=form_data.username, password=form_data.password)
    tokens = await auth_service.login(user_creds, origin=origin, user_agent=user_agent)

    response.set_cookie(
        key=settings.access_token_name,
        value=tokens.access_token,
        httponly=True,
        expires=tokens.access_exp,
    )

    response.set_cookie(
        key=settings.refresh_token_name,
        value=tokens.refresh_token,
        httponly=True,
        expires=tokens.refresh_exp,
    )

    return TokenPair(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,

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
    payload: Annotated[AccessTokenData, Depends(validate_access_token)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    access_token: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
):
    user_id = payload.sub
    response.delete_cookie(key=settings.access_token_name)
    response.delete_cookie(key=settings.refresh_token_name)
    return await auth_service.logout(user_id, access_token, user_agent)

#
#
@router.post(
    '/logout_all',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary='Выход пользователя из всех устройств',
    description='',
)
async def logout_all(
    response: ORJSONResponse,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    payload: Annotated[AccessTokenData, Depends(validate_access_token)],
    user_agent: Annotated[str | None, Header()] = None,

):
    user_id = payload.sub
    await auth_service.logout_all(user_id, user_agent)

    response.delete_cookie(key=settings.access_token_name)
    response.delete_cookie(key=settings.refresh_token_name)

    return {'message': 'All accounts deactivated'}


@router.post(
    '/refresh',
    response_model=TokenPair,
    status_code=status.HTTP_200_OK,
    summary='Обновление access и refresh токенов',
    description='',
)
async def refresh(
    response: ORJSONResponse,
    payload: Annotated[RefreshTokenData, Depends(validate_refresh_token)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    origin: Annotated[str | None, Header()] = None,
    user_agent: Annotated[str | None, Header()] = None,
):
    if origin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Origin header is required',
        )

    user_id = payload.sub
    tokens = await auth_service.refresh(user_id, origin, user_agent)

    response.set_cookie(
        key=settings.access_token_name,
        value=tokens.access_token,
        httponly=True,
        expires=tokens.access_exp,
    )

    response.set_cookie(
        key=settings.refresh_token_name,
        value=tokens.refresh_token,
        httponly=True,
        expires=tokens.refresh_exp,
    )

    return TokenPair(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )
#
#
# @router.post(
#     '/signup_guest',
#     # response_model=,
#     status_code=status.HTTP_200_OK,
#     summary='Регистрация гостевого пользователя',
#     description='''
#     В теле запроса принимает два параметра: логин и пароль.
#     - Если пользователь с таким логином уже существует возвращается ошибка 409 с
#     описанием что такой пользователь уже существует.\n
#     - Если пользователь с таким логином не существует, то он добавляется.\
#     ''',
# )
# async def signup_guest(
#     response: ORJSONResponse,
#     origin: Annotated[str | None, Header()] = None,
#     user_agent: Annotated[str | None, Header()] = None,
#     db: AsyncSession = Depends(get_session),
#     redis: RedisTokenStorage = Depends(get_redis),
# ):
#     if origin is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='Origin header is required',
#         )
#
#     guest_create = User(
#         login=f'login_{uuid4()}',
#         email=f'email_{uuid4()}',
#         password='',
#         first_name=f'guest_{uuid4()}',
#     )
#
#     user = await user_service.create_user(guest_create, db)
#
#     note = History(
#         user_id=user.id,
#         action='/signup_guest',
#         fingerprint=user_agent,
#     )
#     await history_service.make_note(note, db)
#
#     access_token, access_exp = access_token_service.generate_token(origin, user.id, ['guest'])
#     refresh_token, refresh_exp = refresh_token_service.generate_token(origin, user.id)
#     response.set_cookie(key=settings.access_token_name, value=access_token, httponly=True, expires=access_exp)
#     response.set_cookie(key=settings.refresh_token_name, value=refresh_token, httponly=True, expires=refresh_exp)
#
#     await redis.add_valid_rtoken(user.id, refresh_token)
#
#     return {'message': 'Guest created successfully'}
