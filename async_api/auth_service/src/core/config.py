import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import Field
from pydantic_settings import BaseSettings

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    project_name: str = 'movies'
    redis_host: str = Field('127.0.0.1', alias='REDIS_HOST')
    redis_port: int = Field(6379, alias='REDIS_PORT')

    elastic_host: str = Field('127.0.0.1', alias='ELASTIC_HOST')
    elastic_port: int = Field(9200, alias='ELASTIC_PORT')

    pg_user: str = Field('app', alias='DB_USER')
    pg_host: str = Field('127.0.0.1', alias='DB_HOST')
    pg_port: int = Field(5432, alias='DB_PORT')
    pg_password: str = Field('123qwe', alias='DB_PASSWORD')
    pg_name: str = Field('auth_database', alias='DB_NAME')


settings = Settings()