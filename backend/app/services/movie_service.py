from datetime import date

from sqlalchemy.orm import Session

from app.repositories.movie_repository import get_movies
from app.schemas.search import MovieResult


def list_movies(
    db: Session,
    title: str | None = None,
    language: str | None = None,
    genre: str | None = None,
    certification: str | None = None,
    release_date: date | None = None,
    max_duration: int | None = None,
    sort_by: str = "title",
) -> list[MovieResult]:
    movies = get_movies(
        db,
        title=title,
        language=language,
        genre=genre,
        certification=certification,
        release_date=release_date,
        max_duration=max_duration,
        sort_by=sort_by,
    )

    return [
        MovieResult(
            id=movie.id,
            title=movie.title,
            language=movie.language,
            duration_minutes=movie.duration_minutes,
            genre=movie.genre,
            certification=movie.certification,
            release_date=movie.release_date,
            poster_url=movie.poster_url,
        )
        for movie in movies
    ]