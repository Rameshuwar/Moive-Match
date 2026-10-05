from datetime import date as DateType
from datetime import time as TimeType

from pydantic import BaseModel, Field, model_validator


class SearchRequest(BaseModel):
    location: str = Field(
        min_length=1,
        description="District or area where the user wants to watch a movie",
        examples=["Salem"],
    )

    date: DateType = Field(
        description="Date of the movie show",
        examples=["2026-10-03"],
    )

    start_time: TimeType = Field(
        description="Start of the preferred time range",
        examples=["14:00"],
    )

    end_time: TimeType = Field(
        description="End of the preferred time range",
        examples=["19:00"],
    )

    max_price: int = Field(
        gt=0,
        description="Maximum ticket price in INR",
        examples=[100],
    )
    @model_validator(mode="after")
    def validate_time_range(self):
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be earlier than end_time")
        return self


class ShowResult(BaseModel):
    movie: str
    theatre: str
    show_time: TimeType
    ticket_price: int
    available_seats: int


class SearchResponse(BaseModel):
    total_results: int
    results: list[ShowResult]


class MovieResult(BaseModel):
    id: int
    title: str
    language: str
    duration_minutes: int
    genre: str
    certification: str
    release_date: DateType
    poster_url: str | None
