

from fastapi import APIRouter, Depends, status, HTTPException, Query
from schemas.entity import User
from sqlalchemy import select
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from models.entity import UserModel
from services.user_service import user_service
from uuid import UUID

router = APIRouter()



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

#=====================================

@router.get('/users')
async def get_users(db: AsyncSession = Depends(get_session)) -> list[User]:
    users = await user_service.get_users(db)
    return users

@router.post('/signup', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: User, db: AsyncSession = Depends(get_session)) -> User | None:
    return await user_service.create_user(user_create, db)


@router.get('/signin', response_model=User, status_code=status.HTTP_200_OK)
async def login_user(user_login: str, db: AsyncSession = Depends(get_session)):
    db_user = await user_service.get_user_by_login(user_login, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return db_user