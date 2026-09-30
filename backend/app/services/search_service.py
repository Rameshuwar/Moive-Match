from datetime import time

from app.schemas.search import SearchRequest, SearchResponse, ShowResult


def search_shows(request: SearchRequest) -> SearchResponse:

    mock_shows = [
        ShowResult(
            movie="Example Movie",
            theatre="Example Theatre",
            show_time=time(14, 30),
            ticket_price=100,
            available_seats=18,
        ),
        ShowResult(
            movie="Another Movie",
            theatre="Salem Cinema",
            show_time=time(15, 0),
            ticket_price=90,
            available_seats=32,
        ),
        ShowResult(
            movie="Evening Movie",
            theatre="City Theatre",
            show_time=time(18, 30),
            ticket_price=100,
            available_seats=20,
        ),
    ]

    matching_shows = []

    for show in mock_shows:

        if show.ticket_price > request.max_price:
            continue

        if show.available_seats < request.ticket_count:
            continue

        if not (
            request.start_time
            <= show.show_time
            <= request.end_time
        ):
            continue

        matching_shows.append(show)

    return SearchResponse(
        total_results=len(matching_shows),
        results=matching_shows,
    )