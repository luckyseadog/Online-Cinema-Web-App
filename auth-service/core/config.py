from logging import config as logging_config
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)

BASE_DIRECTORY = Path()


class Configs(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    project_name: str = Field(default="auth", alias="PROJECT_NAME")

    pg_name: str = Field(default="", alias="POSTGRES_DB", serialization_alias="DB_NAME")
    pg_user: str = Field(default="", alias="POSTGRES_USER", serialization_alias="DB_USER")
    pg_password: str = Field(default="", alias="POSTGRES_PASSWORD", serialization_alias="DB_PASSWORD")
    pg_host: str = Field(default="", alias="POSTGRES_HOST", serialization_alias="DB_HOST")
    pg_port: int = Field(default=5432, alias="POSTGRES_PORT", serialization_alias="DB_PORT")

    redis_host: str = Field(default="127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")

    access_token_min: int = Field(default=30, alias="ACCESS_TOKEN_MIN")
    refresh_token_min: int = Field(default=2 * 7 * 24 * 60, alias="REFRESH_TOKEN_MIN")

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_name}"


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    authjwt_secret_key: str = Field(default="secret", alias="JWT_SECRET_KEY")
    authjwt_token_location: set[str] = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


class AdminConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    username: str = Field(default="admin", alias="ADMIN_USERNAME")
    password: str = Field(default="admin", alias="ADMIN_PASSWORD")
    right_name: str = Field(default="admin", alias="ADMIN_RIGHT_NAME")
    first_name: str = Field(default="admin", alias="ADMIN_FRIST_NAME")
    last_name: str = Field(default="admin", alias="ADMIN_LAST_NAME")
    email: str = Field(default="admin", alias="ADMIN_EMAIL")


configs = Configs()
jwt_config = JWTConfig()
admin_config = AdminConfig()
