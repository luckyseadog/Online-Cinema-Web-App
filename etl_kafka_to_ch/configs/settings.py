from logging import Logger, getLogger
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIRECTORY = Path()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    kafka_servers: list[str] | str = Field(
        default=["kafka-0:9092", "kafka-1:9092", "kafka-2:9092"], alias="KAFKA_SERVERS"
    )
    kafka_topic: str = Field(default="message", alias="KAFKA_TOPIC")
    kafka_group_id: str = Field(default="cool_id", alias="KAFKA_GROUP_ID")

    ch_host: str = Field(default="clickhouse-node1", alias="CH_HOST")
    ch_port: int = Field(default=8123, alias="CH_PORT")
    ch_database: str = Field(default="example", alias="CH_DATABASE")
    ch_user: str = Field(default="default", alias="CH_USER")
    ch_password: str = Field(default="", alias="CH_PASSWORD")
    ch_table: str = Field(default="event", alias="CH_TABLE")

    batch_size: int = Field(default=1000, alias="BATCH_SIZE")
    run_interval_seconds: int = Field(default=5, alias="RUN_INTERVAL_SECONDS")
    log_level: str = Field(default="info", alias="LOG_LEVEL")

    logger: Logger = getLogger("etl")


settings = Settings()
