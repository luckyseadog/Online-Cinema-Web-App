from logging import config as logging_config
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)

BASE_DIRECTORY = Path()


class Configs(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    project_name: str = Field(alias="PROJECT_NAME")

    mongo_host: str = Field(alias="MONGO_HOST_UGC", serialization_alias="DB_HOST")
    mongo_port: int = Field(alias="MONGO_PORT_UGC", serialization_alias="DB_PORT")
    mongo_name: str = Field(alias="MONGO_NAME_UGC", serialization_alias="DB_NAME")

    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")

    jaeger_on: bool = Field(alias="JAEGER_ON")
    jaeger_host: str = Field(alias="JAEGER_HOST")
    jaeger_port: int = Field(alias="JAEGER_PORT")

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    authjwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    authjwt_token_location: set[str] = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


class MiddlewareConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    update_time: int = Field(alias="UPDATE_TIME")
    update_val: int = Field(alias="UPDATE_VAL")
    capacity: int = Field(alias="CAPACITY")


configs = Configs()  # pyright: ignore[reportCallIssue]
jwt_config = JWTConfig()  # pyright: ignore[reportCallIssue]
middleware_config = MiddlewareConfig()  # pyright: ignore[reportCallIssue]
