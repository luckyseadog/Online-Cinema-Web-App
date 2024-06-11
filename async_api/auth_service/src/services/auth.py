import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from datetime import timedelta, datetime
from typing import Annotated
from schemas.entity import Token, TokenData, UserLogin



SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

pwd_context = CryptContext(schemes=['bcrypt',], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='refresh')

class AuthService:
    async def create_access_token(
            self,
            data: dict,
            expires_delta: timedelta | None = None,
            db: AsyncSession = Depends(get_session)
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = self.get_user(db, token_data.username)
        if user is None:
            raise credentials_exception
        return user


    async def authenticate_user(
            self,
            user_login: UserLogin,
            db: AsyncSession = Depends(get_session)
    ) -> bool:
        user = self.get_user(db, user_login.username)
        if not user:
            return False
        if not self.verify_password(user_login.user_password, user.password_hash):
            return False
        return user

    async def login_for_access_token(self, token: Annotated[str, Depends]) -> Token:
        user = self.authenticate_user(user_name, password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user_name}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


auth_service = AuthService()