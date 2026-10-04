from datetime import date, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.screen import Screen
from app.models.show import Show
from app.models.show_price import ShowPrice
from app.models.theatre import Theatre


def find_shows(
    db: Session,
    location: str,
    show_date: date,
    start_time: time,
    end_time: time,
    max_price: int,
):
    filters = [
        Theatre.district.ilike(f"%{location}%"),
        Show.show_date == show_date,
        Show.show_time >= start_time,
        Show.show_time <= end_time,
        ShowPrice.ticket_price <= max_price,
    ]

    statement = (
        select(
            Movie.title,
            Theatre.name,
            Show.show_time,
            ShowPrice.ticket_price,
            ShowPrice.available_seats,
        )
        .join(Show, Show.movie_id == Movie.id)
        .join(Screen, Show.screen_id == Screen.id)
        .join(Theatre, Screen.theatre_id == Theatre.id)
        .join(ShowPrice, ShowPrice.show_id == Show.id)
        .where(*filters)
        .order_by(Show.show_time)
    )

    return db.execute(statement).all()