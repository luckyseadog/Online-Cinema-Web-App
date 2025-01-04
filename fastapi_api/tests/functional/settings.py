from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    es_host: str = '127.0.0.1'
    es_port: int = 9200

    redis_host: str = '127.0.0.1'
    redis_port: int = 6379

    service_host: str = '127.0.0.1'
    service_port: int = 8000


test_settings = TestSettings()
