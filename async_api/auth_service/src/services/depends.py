from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_session
from services.utils import (
    ALGORITHM,
    SECRET_KEY_ACCESS,
)
from schemas.entity import TokenData

import jwt
from jwt.exceptions import InvalidTokenError
from services.user_service import user_service
from services.token_service import access_token_service
import json

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login',
    scheme_name='JWT',
)


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_session)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail='Could not validate credentials',
#         headers={'WWW-Authenticate': 'Bearer'},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY_ACCESS, algorithms=[ALGORITHM])
#         username: str = payload.get('sub')
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = await user_service.get_user(token_data.username, db)
#     if user is None:
#         raise credentials_exception
#     return user

async def get_current_user(token: str, db: AsyncSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload_str = access_token_service.decode_b64(token.split(".")[1])
        payload = json.loads(payload_str)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await user_service.get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user

