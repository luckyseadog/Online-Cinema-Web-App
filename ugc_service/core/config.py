from logging import config as logging_config
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)

BASE_DIRECTORY = Path()


class Configs(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    project_name: str = "ugc-service"

    mongo_host: str = Field(alias="MONGO_HOST_UGC")
    mongo_port: int = Field(alias="MONGO_PORT_UGC")
    mongo_name: str = Field(alias="MONGO_NAME_UGC")

    redis_host: str = Field(alias="UGC_REDIS_HOST")
    redis_port: int = Field(alias="UGC_REDIS_PORT")

    jaeger_on: bool = Field(alias="JAEGER_ON")
    jaeger_host: str = Field(alias="JAEGER_HOST")
    jaeger_port: int = Field(alias="JAEGER_PORT")

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")

    kafka_boorstrap_server: list[str] | str = Field(alias="KAFKA_BOOTSTRAP_SERVER")
    kafka_topic: str = Field(alias="UGC_KAFKA_TOPIC")

    access_token_min: int = Field(15, alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_weeks: int = Field(1, alias='REFRESH_TOKEN_WEEKS')

    token_secret_key: str = Field('secret', alias='TOKEN_SECRET_KEY')


class MiddlewareConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    update_time: int = Field(alias="UPDATE_TIME")
    update_val: int = Field(alias="UPDATE_VAL")
    capacity: int = Field(alias="CAPACITY")


configs = Configs()  # pyright: ignore[reportCallIssue]
middleware_config = MiddlewareConfig()  # pyright: ignore[reportCallIssue]
