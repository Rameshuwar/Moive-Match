from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.movie import Movie


def get_movies(
    db: Session,
    title: str | None = None,
    language: str | None = None,
    genre: str | None = None,
    certification: str | None = None,
    release_date: date | None = None,
    max_duration: int | None = None,
    sort_by: str = "title",
) -> list[Movie]:
    statement = select(Movie)

    if title:
        statement = statement.where(
            Movie.title.ilike(f"%{title}%")
        )

    if language:
        statement = statement.where(
            Movie.language.ilike(f"%{language}%")
        )

    if genre:
        statement = statement.where(
            Movie.genre.ilike(f"%{genre}%")
        )

    if certification:
        statement = statement.where(
            Movie.certification.ilike(f"%{certification}%")
        )

    if release_date:
        statement = statement.where(
            Movie.release_date == release_date
        )

    if max_duration is not None:
        statement = statement.where(
            Movie.duration_minutes <= max_duration
        )

    if sort_by == "release_date":
        statement = statement.order_by(
            Movie.release_date.desc()
        )
    elif sort_by == "duration":
        statement = statement.order_by(
            Movie.duration_minutes
        )
    else:
        statement = statement.order_by(
            Movie.title
        )

    return list(db.scalars(statement).all())