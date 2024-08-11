from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


BASE_DIRECTORY = Path()


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    es_host: str = Field(default="127.0.0.1", alias="ELASTIC_HOST")
    es_port: int = Field(default=9200, alias="ELASTIC_PORT")
    es_index: str = Field(default="movies", alias="ELASTIC_INDEX")
    es_id_field: str = Field(default="uuid", alias="ELASTIC_ID_FIELD")
    es_index_mapping: dict[Any, Any] = Field(default={}, alias="ELASTIC_INDEX_MAPPING")

    redis_host: str = Field(default="127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")

    service_host: str = Field(default="127.0.0.1", alias="SERVICE_HOST")
    service_port: int = Field(default=8000, alias="SERVICE_PORT")

    @property
    def elastic_dsn(self) -> str:
        return f"http://{self.es_host}:{self.es_port}/"

    @property
    def service_url(self) -> str:
        return f"http://{self.service_host}:{self.service_port}/"


test_settings = TestSettings()
