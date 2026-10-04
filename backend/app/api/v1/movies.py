from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.search import MovieResult
from app.services.movie_service import list_movies


router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "",
    response_model=list[MovieResult],
)
async def get_movies(
    title: str | None = Query(
        default=None,
        min_length=1,
        description="Optional movie title to search for",
    ),
    language: str | None = Query(
        default=None,
        min_length=1,
        description="Optional movie language to filter by",
    ),
    genre: str | None = Query(
        default=None,
        min_length=1,
        description="Optional movie genre to filter by",
    ),
    certification: str | None = Query(
        default=None,
        min_length=1,
        description="Optional movie certification to filter by",
    ),
    release_date: date | None = Query(
        default=None,
        description="Optional movie release date to filter by",
    ),
    max_duration: int | None = Query(
        default=None,
        gt=0,
        description="Optional maximum movie duration in minutes",
    ),
    sort_by: Literal["title", "release_date", "duration"] = Query(
        default="title",
        description="Movie sorting option",
    ),
    db: Session = Depends(get_db),
):
    return list_movies(
        db,
        title=title,
        language=language,
        genre=genre,
        certification=certification,
        release_date=release_date,
        max_duration=max_duration,
        sort_by=sort_by,
    )