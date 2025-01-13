import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = 'payment-service'
    stripe_api_key: str = "sk_test_51Qffa2E1UjG6eS2xle6NK04Uafj9XSwY365aOSfKzTuAHhNYDtvXzbF8k3W4OZH3ptCCVLAYNtMpccYZusXkgyEo00tI79XvhV"
    # Use the secret provided by Stripe CLI for local testing
    # or your webhook endpoint's secret.
    webhook_secret: str = "whsec_Fvi7mBOVEisnkTzv6Yek5HAWQKIqZMuh"
    success_url: str = 'http://localhost:80/payments/v1/success_response'
    cancel_url: str = 'http://localhost:80/payments/v1/cancel_response'

    redis_host: str = Field('redis-payments', alias='PAYMENT_REDIS_HOST')
    redis_port: int = Field(6379, alias='PAYMENT_REDIS_PORT')

    access_token_min: int = Field(15, alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_weeks: int = Field(1, alias='REFRESH_TOKEN_WEEKS')

    token_secret_key: str = Field('secret', alias='TOKEN_SECRET_KEY')


settings = Settings()
