from datetime import date as DateType
from datetime import time as TimeType

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    location: str = Field(
        min_length=1,
        description="City or area where the user wants to watch the movie",
        examples=["Salem"],
    )

    date: DateType = Field(
        description="Date of the movie show",
        examples=["2026-09-26"],
    )

    start_time: TimeType = Field(
        description="Start of the preferred time range",
        examples=["14:00"],
    )

    end_time: TimeType = Field(
        description="End of the preferred time range",
        examples=["16:00"],
    )

    max_price: int = Field(
        gt=0,
        description="Maximum ticket price in INR",
        examples=[100],
    )

    ticket_count: int = Field(
        gt=0,
        description="Number of tickets required",
        examples=[2],
    )


class ShowResult(BaseModel):
    movie: str
    theatre: str
    show_time: TimeType
    ticket_price: int
    available_seats: int


class SearchResponse(BaseModel):
    total_results: int
    results: list[ShowResult]