from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.screen import Screen
from app.models.show import Show
from app.models.show_price import ShowPrice
from app.models.theatre import Theatre
from app.schemas.search import SearchRequest, SearchResponse, ShowResult


def search_shows(
    request: SearchRequest,
    db: Session,
) -> SearchResponse:

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
        .where(
            Theatre.district.ilike(request.location),
            Show.show_date == request.date,
            Show.show_time >= request.start_time,
            Show.show_time <= request.end_time,
            ShowPrice.ticket_price <= request.max_price,
            ShowPrice.available_seats >= request.ticket_count,
        )
        .order_by(Show.show_time)
    )

    rows = db.execute(statement).all()

    results = [
        ShowResult(
            movie=row.title,
            theatre=row.name,
            show_time=row.show_time,
            ticket_price=row.ticket_price,
            available_seats=row.available_seats,
        )
        for row in rows
    ]

    return SearchResponse(
        total_results=len(results),
        results=results,
    )