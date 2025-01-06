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

    mongo_host_ugc: str = Field(alias="MONGO_HOST_UGC", serialization_alias="DB_HOST_UGC")
    mongo_port_ugc: int = Field(alias="MONGO_PORT_UGC", serialization_alias="DB_PORT_UGC")
    mongo_name: str = Field(alias="MONGO_NAME_UGC", serialization_alias="DB_NAME_UGC")

    pg_name_admin: str = Field(alias="POSTGRES_DB_ADMIN", serialization_alias="DB_NAME_ADMIN")
    pg_user_admin: str = Field(alias="POSTGRES_USER_ADMIN", serialization_alias="DB_USER_ADMIN")
    pg_password_admin: str = Field(alias="POSTGRES_PASSWORD_ADMIN", serialization_alias="DB_PASSWORD_ADMIN")
    pg_host_admin: str = Field(alias="POSTGRES_HOST_ADMIN", serialization_alias="DB_HOST_ADMIN")
    pg_port_admin: int = Field(alias="POSTGRES_PORT_ADMIN", serialization_alias="DB_PORT_ADMIN")

    kafka_topic: str = Field(alias="KAFKA_TOPIC")
    kafka_boorstrap_server: list[str] | str = Field(alias="KAFKA_BOOTSTRAP_SERVER")
    kafka_auto_offset_reset: str = Field(alias="AUTO_OFFSET_RESET")
    kafka_group_id: str = Field(alias="KAFKA_GROUP_ID")

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")

    @property
    def postgres_dsn_admin(self) -> str:
        return f"postgresql+psycopg://{self.pg_user_admin}:{self.pg_password_admin}@{self.pg_host_admin}:{self.pg_port_admin}/{self.pg_name_admin}"


configs = Configs()  # pyright: ignore[reportCallIssue]
