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

    token_secret_key: str = Field('secret', alias='TOKEN_SECRET_KEY')

    access_token_min: int = Field(15, alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_weeks: int = Field(1, alias='REFRESH_TOKEN_WEEKS')


settings = Settings()
