from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_url: str = Field('https://api.brevo.com/v3/smtp/email', alias='API_URL')
    api_key: str = Field(
        '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', alias='API_KEY'
    )
    kafka_boorstrap_server: str = Field(default="kafka-0:9092", alias="KAFKA_BOOTSTRAP_SERVER")
    kafka_topics: str = 'welcome-topic,new-movies-topic,sale-topic'
    kafka_auto_offset_reset: str = Field(default="earliest", alias="AUTO_OFFSET_RESET")
    kafka_group_id: str = Field(default="main-group", alias="GROUP_ID")


settings = Settings()
