from logging import config as logging_config
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)


BASE_DIRECTORY = Path()


class Configs(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    project_name: str = Field(default="kafka-consumer", alias="PROJECT_NAME")

    pg_name_ugc: str = Field(default="ugc_database", alias="POSTGRES_DB_UGC", serialization_alias="DB_NAME_UGC")
    pg_user_ugc: str = Field(default="postgres", alias="POSTGRES_USER_UGC", serialization_alias="DB_USER_UGC")
    pg_password_ugc: str = Field(default="123qwe", alias="POSTGRES_PASSWORD_UGC", serialization_alias="DB_PASSWORD_UGC")
    pg_host_ugc: str = Field(default="postgres_db_ugc", alias="POSTGRES_HOST_UGC", serialization_alias="DB_HOST_UGC")
    pg_port_ugc: int = Field(default=5432, alias="POSTGRES_PORT_UGC", serialization_alias="DB_PORT_UGC")

    pg_name_admin: str = Field(
        default="movies_database", alias="POSTGRES_DB_ADMIN", serialization_alias="DB_NAME_ADMIN"
    )
    pg_user_admin: str = Field(default="postgres", alias="POSTGRES_USER_ADMIN", serialization_alias="DB_USER_ADMIN")
    pg_password_admin: str = Field(
        default="123qwe", alias="POSTGRES_PASSWORD_ADMIN", serialization_alias="DB_PASSWORD_ADMIN"
    )
    pg_host_admin: str = Field(default="postgres_db", alias="POSTGRES_HOST_ADMIN", serialization_alias="DB_HOST_ADMIN")
    pg_port_admin: int = Field(default=5432, alias="POSTGRES_PORT_ADMIN", serialization_alias="DB_PORT_ADMIN")

    kafka_topic: str = Field(default="postgres", alias="KAFKA_TOPIC")
    kafka_boorstrap_server: list[str] | str = Field(
        default=["kafka-0:9092", "kafka-1:9092", "kafka-2:9092"], alias="KAFKA_BOOTSTRAP_SERVER"
    )
    kafka_auto_offset_reset: str = Field(default="earliest", alias="AUTO_OFFSET_RESET")
    kafka_group_id: str = Field(default="sample-group", alias="GROUP_ID")

    @property
    def postgres_dsn_ugc(self) -> str:
        return f"postgresql+psycopg://{self.pg_user_ugc}:{self.pg_password_ugc}@{self.pg_host_ugc}:{self.pg_port_ugc}/{self.pg_name_ugc}"

    @property
    def postgres_dsn_admin(self) -> str:
        return f"postgresql+psycopg://{self.pg_user_admin}:{self.pg_password_admin}@{self.pg_host_admin}:{self.pg_port_admin}/{self.pg_name_admin}"


configs = Configs()
