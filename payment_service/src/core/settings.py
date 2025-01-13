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
    success_url: str = 'http://localhost:8000/pay/v1/success_response'
    cancel_url: str = 'http://localhost:8000/pay/v1/cancel_response'



settings = Settings()
