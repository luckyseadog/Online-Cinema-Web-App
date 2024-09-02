from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from testdata.es_mapping import GENRE_SCHEMES_INDEX_ES, MOVIES_SCHEMES_INDEX_ES, PERSON_SCHEMES_INDEX_ES


BASE_DIRECTORY = Path()


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    es_host: str = Field(default="127.0.0.1", alias="ELASTIC_HOST")
    es_port: int = Field(default=9200, alias="ELASTIC_PORT")
    es_id_field: str = Field(default="uuid", alias="ELASTIC_ID_FIELD")
    es_index_movies: str = Field(default="movies", alias="ELASTIC_INDEX_MOVIES")
    es_index_mapping_movies: dict[Any, Any] = Field(
        default=MOVIES_SCHEMES_INDEX_ES, alias="ELASTIC_INDEX_MAPPING_MOVIES"
    )
    es_index_genres: str = Field(default="genres", alias="ELASTIC_INDEX_GENRES")
    es_index_mapping_genres: dict[Any, Any] = Field(
        default=GENRE_SCHEMES_INDEX_ES, alias="ELASTIC_INDEX_MAPPING_GENRES"
    )
    es_index_persons: str = Field(default="persons", alias="ELASTIC_INDEX_PERSONS")
    es_index_mapping_persons: dict[Any, Any] = Field(
        default=PERSON_SCHEMES_INDEX_ES, alias="ELASTIC_INDEX_MAPPING_PERSONS"
    )

    redis_host: str = Field(default="127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")

    service_host: str = Field(default="127.0.0.1", alias="SERVICE_HOST")
    service_port: int = Field(default=8000, alias="SERVICE_PORT")

    pg_name: str = Field(alias="POSTGRES_DB", serialization_alias="DB_NAME")
    pg_user: str = Field(alias="POSTGRES_USER", serialization_alias="DB_USER")
    pg_password: str = Field("", alias="POSTGRES_PASSWORD", serialization_alias="DB_PASSWORD")
    pg_host: str = Field("", alias="POSTGRES_HOST", serialization_alias="DB_HOST")
    pg_port: int = Field(5432, alias="POSTGRES_PORT", serialization_alias="DB_PORT")

    @property
    def elastic_dsn(self) -> str:
        return f"http://{self.es_host}:{self.es_port}/"

    @property
    def service_url(self) -> str:
        return f"http://{self.service_host}:{self.service_port}/"

    @property
    def postgres_dsn(self) -> dict[str, str | int]:
        return {
            "dbname": self.pg_name,
            "user": self.pg_user,
            "password": self.pg_password,
            "host": self.pg_host,
            "port": self.pg_port,
        }


test_settings = TestSettings()
