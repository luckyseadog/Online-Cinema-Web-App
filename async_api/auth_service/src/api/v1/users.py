

from fastapi import APIRouter, Depends, status, HTTPException, Query
from schemas.entity import UserCreate, UserInDB
from sqlalchemy import select
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from models.entity import User
from services.user import user_service
from uuid import UUID

router = APIRouter()


@router.post('/signup', response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_session)) -> UserInDB | None:
    return await user_service.create_user(user_create, db)


@router.get('/signin', response_model=UserInDB, status_code=status.HTTP_200_OK)
async def login_user(user_login: str, db: AsyncSession = Depends(get_session)):
    db_user = await user_service.get_user_by_login(user_login, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return db_user


@router.delete('/')
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_session)):
    db_user = await user_service.delete_user(user_id, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return db_user


@router.patch('/')
async def change_user(user_id: UUID, db: AsyncSession = Depends(get_session)):
    db_user = await user_service.update_user(user_id, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return db_user

@router.get('/access')
async def get_access(db: AsyncSession = Depends(get_session)):
    return {"message": "get new tokens"}


@router.get('/history')
async def get_history(db: AsyncSession = Depends(get_session)):
    return {"message": "history of user"}