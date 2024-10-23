from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class Event(BaseModel):
    user_id: UUID = Field(description="UUID")
    film_id: str | None = Field(default=None, description="String NULL")
    prev_qual: int | None = Field(default=None, description="int NULL")
    new_qual: int | None = Field(default=None, description="int NULL")
    element_id: str | None = Field(default=None, description="String NULL")
    group_id: str | None = Field(default=None, description="String NULL")
    time: str | None = Field(default=None, description="String NULL")
    action: Literal["stop", "pause", "review", "rate", "favourite", "unfavourite"] | None = Field(
        default=None, description="Enum('stop', 'pause', 'review', 'rate', 'favourite', 'unfavourite') NULL"
    )
    feedback: str | None = Field(default=None, description="String NULL")
    review: str | None = Field(default=None, description="String NULL")
    rating: int | None = Field(default=None, description="int NULL")
    filter_id_genre: list[str] = Field(default=[], description="Array(String)")
    filter_rating: int | None = Field(default=None, description="int NULL")
    filter_id_actor: list[str] = Field(default=[], description="Array(String)")
    film_curr_time: int | None = Field(default=None, description="int NULL")
    film_abs_time: int | None = Field(default=None, description="int NULL")
    url: str | None = Field(default=None, description="String NULL")
    spent_time: int | None = Field(default=None, description="int NULL")
    timestamp: datetime = Field(description="DateTime", default_factory=datetime.now)

    @field_validator("filter_id_genre", "filter_id_actor")
    @classmethod
    def validate_x(cls, v: list[str] | None) -> list[str]:
        return [] if v is None else v
