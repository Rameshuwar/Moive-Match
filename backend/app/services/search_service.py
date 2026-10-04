from sqlalchemy.orm import Session

from app.repositories.search_repository import find_shows
from app.schemas.search import SearchRequest, SearchResponse, ShowResult


def search_shows(
    request: SearchRequest,
    db: Session,
) -> SearchResponse:
    rows = find_shows(
        db=db,
        location=request.location,
        show_date=request.date,
        start_time=request.start_time,
        end_time=request.end_time,
        max_price=request.max_price,
    )

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