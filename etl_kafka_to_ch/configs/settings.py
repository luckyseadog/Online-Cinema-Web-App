from logging import Logger, getLogger
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIRECTORY = Path()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    kafka_servers: list[str] | str = Field(alias="KAFKA_SERVERS")
    kafka_topic: str = Field(alias="KAFKA_TOPIC")
    kafka_group_id: str = Field(alias="KAFKA_GROUP_ID")

    ch_host: str = Field(alias="CH_HOST")
    ch_port: int = Field(alias="CH_PORT")
    ch_database: str = Field(alias="CH_DATABASE")
    ch_user: str = Field(alias="CH_USER")
    ch_password: str = Field(alias="CH_PASSWORD")
    ch_table: str = Field(alias="CH_TABLE")

    batch_size: int = Field(alias="BATCH_SIZE")
    run_interval_seconds: int = Field(alias="RUN_INTERVAL_SECONDS")
    log_level: str = Field(alias="LOG_LEVEL")

    logger: Logger = getLogger("etl")

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")


settings = Settings()  # pyright: ignore[reportCallIssue]
