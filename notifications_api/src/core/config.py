from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_url: str = Field('https://api.brevo.com/v3/smtp/email', alias='API_URL')
    api_key: str = Field(
        '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', alias='API_KEY'
    )

    redis_host: str = Field(default="redis", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")

    update_time: int = Field(default=20, alias="UPDATE_TIME")
    update_val: int = Field(default=1, alias="UPDATE_VAL")
    capacity: int = Field(default=1, alias="CAPACITY")

    kafka_boorstrap_server: str = Field(default="kafka-0:9092", alias="KAFKA_BOOTSTRAP_SERVER")
    auth_secret_key: str = Field("secret", alias="AUTH_SECRET_KEY")

    access_token_min: int = Field(15, alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_weeks: int = Field(1, alias='REFRESH_TOKEN_WEEKS')


settings = Settings()
