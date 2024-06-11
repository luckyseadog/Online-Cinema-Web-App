
from fastapi import APIRouter
from fastapi import status
from services.auth import auth_service
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from schemas.entity import UserLogin
router = APIRouter()


@router.post(
    '/signup',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary="Регистрация пользователя",
    description='''
    В теле запроса принимает два параметра: логин и пароль. 
    - Если пользователь с таким логином уже существует возвращается ошибка 409 с описанием что такой пользователь уже существует.\n
    - Если пользователь с таким логином не существует, то он добавляется.\n
    '''
)
async def signup():
    return {"message": "signup"}

@router.post(
    '/login',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary="Аутентификация пользователя",
    description='''
    В теле запроса принимает два параметра: логин и пароль. 
    - Если пользователь с таким логином и паролем не существует возвращается ошибка 404 с описанием что такого пользователя нет.\n
    - Если пользователь с таким логином и паролем существует, то он
    '''
)
async def login(userlogin: UserLogin, db: AsyncSession = Depends(get_session)):
    res = auth_service.authenticate_user(userlogin, db)
    return res

@router.post(
    '/logout',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary='Выход пользователя',
    description=''
)
async def logout():
    return {"message": "logout"}


@router.post(
    '/logout_all',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary='Выход пользователя из всех устройств',
    description=''
)
async def logout_all():
    return {"message": "logout_all"}


@router.post(
    '/refresh',
#     response_model=,
    status_code=status.HTTP_200_OK,
    summary='Обновление access и refresh токенов',
    description=''
)
async def refresh():
    auth_service

@router.post(
    '/signup_guest',
    # response_model=,
    status_code=status.HTTP_200_OK,
    summary="Регистрация гостевого пользователя",
    description='''
    В теле запроса принимает два параметра: логин и пароль. 
    - Если пользователь с таким логином уже существует возвращается ошибка 409 с описанием что такой пользователь уже существует.\n
    - Если пользователь с таким логином не существует, то он добавляется.\
    '''
)
async def signup_guest():
    return {"message": "signup_guest"}