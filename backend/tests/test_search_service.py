from app.schemas.search import SearchRequest
from app.services.search_service import search_shows


def test_search_returns_matching_show(db):
    request = SearchRequest(
        location="Salem",
        date="2026-10-03",
        start_time="14:00",
        end_time="19:00",
        max_price=100,
    )

    response = search_shows(request, db)

    assert response.total_results == 1
    assert len(response.results) == 1

    result = response.results[0]

    assert result.movie == "Test Movie"
    assert result.theatre == "Test Theatre"
    assert str(result.show_time) == "15:00:00"
    assert result.ticket_price == 90
    assert result.available_seats == 32


def test_search_respects_max_price(db):
    request = SearchRequest(
        location="Salem",
        date="2026-10-03",
        start_time="14:00",
        end_time="19:00",
        max_price=80,
    )

    response = search_shows(request, db)

    assert response.total_results == 0
    assert response.results == []


def test_search_respects_location(db):
    request = SearchRequest(
        location="Chennai",
        date="2026-10-03",
        start_time="14:00",
        end_time="19:00",
        max_price=100,
    )

    response = search_shows(request, db)

    assert response.total_results == 0
    assert response.results == []


def test_search_respects_date(db):
    request = SearchRequest(
        location="Salem",
        date="2026-10-04",
        start_time="14:00",
        end_time="19:00",
        max_price=100,
    )

    response = search_shows(request, db)

    assert response.total_results == 0
    assert response.results == []


def test_search_respects_time_range(db):
    request = SearchRequest(
        location="Salem",
        date="2026-10-03",
        start_time="16:00",
        end_time="19:00",
        max_price=100,
    )

    response = search_shows(request, db)

    assert response.total_results == 0
    assert response.results == []


def test_search_returns_seats_for_each_specific_price(db):
    from app.models import ShowPrice

    show_id = db.query(ShowPrice).first().show_id

    db.add(
        ShowPrice(
            show_id=show_id,
            ticket_price=100,
            available_seats=18,
        )
    )
    db.commit()

    request = SearchRequest(
        location="Salem",
        date="2026-10-03",
        start_time="14:00",
        end_time="19:00",
        max_price=100,
    )

    response = search_shows(request, db)

    assert response.total_results == 2

    prices_and_seats = {
        result.ticket_price: result.available_seats
        for result in response.results
    }

    assert prices_and_seats == {
        90: 32,
        100: 18,
    }


def test_search_returns_seats_for_each_specific_price(db):
    from app.models import ShowPrice

    show_id = db.query(ShowPrice).first().show_id

    db.add(
        ShowPrice(
            show_id=show_id,
            ticket_price=100,
            available_seats=18,
        )
    )
    db.commit()

    request = SearchRequest(
        location="Salem",
        date="2026-10-03",
        start_time="14:00",
        end_time="19:00",
        max_price=100,
    )

    response = search_shows(request, db)

    assert response.total_results == 2

    prices_and_seats = {
        result.ticket_price: result.available_seats
        for result in response.results
    }

    assert prices_and_seats == {
        90: 32,
        100: 18,
    }
