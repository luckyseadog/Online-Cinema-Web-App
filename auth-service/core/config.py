from logging import config as logging_config
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)

BASE_DIRECTORY = Path()


class Configs(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    project_name: str = Field(default="auth", alias="PROJECT_NAME")

    pg_name: str = Field(default="", alias="POSTGRES_DB", serialization_alias="DB_NAME")
    pg_user: str = Field(default="", alias="POSTGRES_USER", serialization_alias="DB_USER")
    pg_password: str = Field(default="", alias="POSTGRES_PASSWORD", serialization_alias="DB_PASSWORD")
    pg_host: str = Field(default="", alias="POSTGRES_HOST", serialization_alias="DB_HOST")
    pg_port: int = Field(default=5432, alias="POSTGRES_PORT", serialization_alias="DB_PORT")

    redis_host: str = Field(default="127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")

    access_token_min: int = Field(default=30, alias="ACCESS_TOKEN_MIN")
    refresh_token_min: int = Field(default=2 * 7 * 24 * 60, alias="REFRESH_TOKEN_MIN")

    iters_password: int = Field(default=100_000, alias="ITERS_PASSWORD")
    hash_name_password: str = Field(default="sha256", alias="HASH_NAME_PASSWORD")

    jaeger_on: bool = Field(default=True, alias="JAEGER_ON")
    jaeger_host: str = Field(default="127.0.0.1", alias="JAEGER_HOST")
    jaeger_port: int = Field(default=6831, alias="JAEGER_PORT")

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_name}"


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    authjwt_secret_key: str = Field(default="secret", alias="JWT_SECRET_KEY")
    authjwt_token_location: set[str] = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


class AdminConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    username: str = Field(default="admin", alias="ADMIN_USERNAME")
    password: str = Field(default="admin", alias="ADMIN_PASSWORD")
    right_name: str = Field(default="admin", alias="ADMIN_RIGHT_NAME")
    first_name: str = Field(default="admin", alias="ADMIN_FRIST_NAME")
    last_name: str = Field(default="admin", alias="ADMIN_LAST_NAME")
    email: str = Field(default="admin", alias="ADMIN_EMAIL")


class OAuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    yandex_scope: str = Field(default=r"login:email%20login:info", alias="YANDEX_SCOPE")
    yandex_state: str = Field(default=r"123qwe", alias="YANDEX_STATE")
    yandex_client_id: str = Field(default=r"2da216bbe9af4bc8a1f7caec1eec7d7a", alias="YANDEX_CLIENT_ID")
    yandex_client_secret: str = Field(default=r"a9d8d6ff93024327ac8648eb2285703e", alias="YANDEX_CLIENT_SECRET")
    yandex_redirect_uri: str = Field(
        default=r"http://127.0.0.1:90/auth/v1/oauth/ya/oauth2callback", alias="YANDEX_REDIRECT_URI"
    )

    google_scope: str = Field(
        default=r"https://www.googleapis.com/auth/userinfo.email%20https://www.googleapis.com/auth/userinfo.profile",
        alias="GOOGLE_SCOPE",
    )
    google_state: str = Field(default=r"123qwe", alias="GOOGLE_STATE")
    google_client_id: str = Field(
        default=r"885218518483-7orcdsgm32s1mq7sphrc957a63hpj7tb.apps.googleusercontent.com", alias="GOOGLE_CLIENT_ID"
    )
    google_client_secret: str = Field(default=r"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", alias="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(
        default=r"http://127.0.0.1:90/auth/v1/oauth/go/oauth2callback", alias="GOOGLE_REDIRECT_URI"
    )


class MiddlewareConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    update_time: int = Field(default=30, alias="UPDATE_TIME")
    update_val: int = Field(default=10, alias="UPDATE_VAL")
    capacity: int = Field(default=10, alias="CAPACITY")


configs = Configs()
jwt_config = JWTConfig()
admin_config = AdminConfig()
oauth_config = OAuthConfig()
middleware_config = MiddlewareConfig()
