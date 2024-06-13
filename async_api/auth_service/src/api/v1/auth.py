from fastapi import APIRouter
from fastapi import status, HTTPException
from services.auth import auth_service
from services.user import user_service
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from schemas.entity import UserCreate
from fastapi.security import OAuth2PasswordRequestForm


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
async def signup(user_create: UserCreate, db: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(user_create.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='email already exists')
    user = await user_service.get_user_by_login(user_create.login)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='login already exists')

    return await user_service.create_user(user_create, db)


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
        db: AsyncSession = Depends(get_session),
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    res = await auth_service.login(form_data, db)
    return res

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
async def logout():
    pass


@router.post(
    '/logout_all',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary='Выход пользователя из всех устройств',
    description='',
)
async def logout_all():
    return {'message': 'logout_all'}


@router.post(
    '/refresh',
    #     response_model=,
    status_code=status.HTTP_200_OK,
    summary='Обновление access и refresh токенов',
    description='',
)
async def refresh():
    pass

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
async def signup_guest():
    return {'message': 'signup_guest'}
