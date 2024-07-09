from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    root_path: str = 'http://localhost:8000/api/v1/auth'

    redis_host: str = '127.0.0.1'
    redis_port: int = 6379

    auth_db: str = 'auth_db'
    auth_db_host: str = '127.0.0.1'
    auth_db_port: int = 5432
    auth_db_user: str = 'auth_user'
    auth_db_password: str = 'qwerty'

    sa_login: str = 'superadmin'
    sa_password: str = 'admin'
    sa_firstname: str = 'admin'
    sa_lastname: str = 'admin'
    sa_email: str = 'superadmin@admin.com'

    role_admin: str = 'admin'
    role_super_admin: str = 'superadmin'
    role_user: str = 'user'
    role_subscriber: str = 'subscriber'
    role_guest: str = 'guest'

    # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


auth_test_settings = Settings()
