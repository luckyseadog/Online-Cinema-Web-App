from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from services.user_service import user_service
from services.password_service import password_service
from fastapi import HTTPException
from schemas.entity import UserCredentials
import logging


# SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
# ALGORITHM = 'HS256'
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    async def login(self, user_creds: UserCredentials, db: AsyncSession) -> bool:
        user = await user_service.get_user_by_login(user_creds.login, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect username or password',
            )

        hash_password = user_creds.password
        target_password = user.password
        logging.warn(f'{hash_password}------{target_password}')

        if not password_service.check_password(hash_password, target_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect username or password',
            )

        return True


auth_service = AuthService()

# def _create_access_token(
#         self,
#         data: dict,
#         expires_delta: timedelta | None = None,
# ):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({'exp': expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def _authenticate_user(
#         self,
#         user_login: UserLogin,
#         db: AsyncSession,
# ) -> bool:
#     user = await user_service.get_user_by_login(user_login.username, db)
#     if not user:
#         return False
#     if not self._verify_password(user_login.password, user.password):
#         return False
#     return user

# async def login_for_access_token(
#     self,
#     user_login: UserLogin,
#     # token: Annotated[str, Depends],
#     db: AsyncSession,
# ) -> Token:
#     user = await self._authenticate_user(user_login, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Incorrect username or password',
#             headers={'WWW-Authenticate': 'Bearer'},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = self._create_access_token(
#         data={'sub': user_login.username},
#         expires_delta=access_token_expires,
#     )
#     return {'access_token': access_token, 'token_type': 'bearer'}

# async def login(
#         self,
#         form_data: OAuth2PasswordRequestForm = Depends(),
#         db: AsyncSession = Depends(get_session),
# ) -> Token:
#     user = await user_service.get_user_by_login(form_data.username, db)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='Incorrect username or password',
#         )

#     hash_password = user.password
#     if not verify_password(form_data.password, hash_password):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='Incorrect username or password',
#         )

#     return {
#         'access_token': create_access_token(user.id),
#         'refresh_token': create_refresh_token(user.id),
#     }
