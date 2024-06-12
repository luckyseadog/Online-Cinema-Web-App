from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_session

import jwt
from datetime import datetime, timedelta, timezone


ACCESS_TOKEN_EXPIRE_MIN = 10
REFRESH_TOKEN_EXPIRE_MIN = 60 * 24 * 7
SECRET_KEY_ACCESS="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
SECRET_KEY_REFRESH="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM="HS256"

pwd_context = CryptContext(schemes=['bcrypt',], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(sub: str | None,  exp_delta: int = None) -> str:
    if exp_delta is not None:
        exp_delta = datetime.now(timezone.utc) + exp_delta
    else:
        exp_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode = {'exp': exp_delta, 'sub': str(sub)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_ACCESS, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(sub: str | None, exp_delta: int = None) -> str:
    if exp_delta is not None:
        exp_delta = datetime.now(timezone.utc) + exp_delta
    else:
        exp_delta = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MIN)
    to_encode = {'exp': exp_delta, 'sub': str(sub)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)
    return encoded_jwt
