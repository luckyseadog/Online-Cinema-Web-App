import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from datetime import timedelta, datetime
from typing import Annotated
from schemas.entity import Token, TokenData, UserLogin, UserCredentials, TokenPair
from services.password_service import password_service
from services.token_service import access_token_service, refresh_token_service
from datetime import timezone
from fastapi import status
from services.user_service import user_service
from fastapi import HTTPException
from services.utils import pwd_context, oauth2_scheme, get_password_hash
# from fastapi.security import OAuth2PasswordRequestForm
from services.utils import create_access_token, create_refresh_token, verify_password, get_password_hash


SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


class AuthService:
    def _create_access_token(
            self,
            data: dict,
            expires_delta: timedelta | None = None,
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt






    async def _authenticate_user(
            self,
            user_login: UserLogin,
            db: AsyncSession = Depends(get_session)
    ) -> bool:
        user = await user_service.get_user_by_login(user_login.username, db)
        if not user:
            return False
        if not self._verify_password(user_login.password, user.password):
            return False
        return user

    async def login_for_access_token(self,
                                     user_login: UserLogin,
                                     # token: Annotated[str, Depends],
                                     db: AsyncSession= Depends(get_session)) -> Token:
        user = await self._authenticate_user(user_login, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            data={"sub": user_login.username},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def login(self, user_creds: UserCredentials, db: AsyncSession = Depends(get_session)) -> bool:
        user = await user_service.get_user_by_login(user_creds.login, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
            )

        hash_password = password_service.compute_hash(user_creds.password)
        target_password = user.password
        if not password_service.check_password(hash_password, target_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
            )

        return True




auth_service = AuthService()