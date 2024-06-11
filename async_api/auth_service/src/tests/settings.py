from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    service_host: str = '127.0.0.1'
    service_port: int = 8000

    redis_host: str = '127.0.0.1'
    redis_port = 6379

    pg_host: str = '127.0.0.1'
    pg_port: int = 5432
    pg_user: str = 'app'
    pg_password: str = '123qwe'
    pg_name: str = 'auth_database'

test_settings = TestSettings()