from logging import config as logging_config
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)

BASE_DIRECTORY = Path()


class Configs(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    project_name: str = Field(default="ugc-service", alias="PROJECT_NAME")

    pg_name: str = Field(default="ugc_database", alias="POSTGRES_DB", serialization_alias="DB_NAME")
    pg_user: str = Field(default="postgres", alias="POSTGRES_USER", serialization_alias="DB_USER")
    pg_password: str = Field(default="", alias="POSTGRES_PASSWORD", serialization_alias="DB_PASSWORD")
    pg_host: str = Field(default="postgres_db_ugc", alias="POSTGRES_HOST", serialization_alias="DB_HOST")
    pg_port: int = Field(default=5432, alias="POSTGRES_PORT", serialization_alias="DB_PORT")

    redis_host: str = Field(default="127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")

    jaeger_on: bool = Field(default=True, alias="JAEGER_ON")
    jaeger_host: str = Field(default="127.0.0.1", alias="JAEGER_HOST")
    jaeger_port: int = Field(default=6831, alias="JAEGER_PORT")

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_name}"


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    authjwt_secret_key: str = Field(default="secret", alias="JWT_SECRET_KEY")
    authjwt_token_location: set[str] = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


class MiddlewareConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    update_time: int = Field(default=30, alias="UPDATE_TIME")
    update_val: int = Field(default=10, alias="UPDATE_VAL")
    capacity: int = Field(default=10, alias="CAPACITY")


configs = Configs()
jwt_config = JWTConfig()
middleware_config = MiddlewareConfig()
