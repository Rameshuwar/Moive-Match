from app.schemas.search import SearchRequest


def test_valid_search_request():
    request = SearchRequest(
        location="Salem",
        date="2026-10-03",
        start_time="14:00",
        end_time="19:00",
        max_price=100,
    )

    assert request.location == "Salem"
    assert request.max_price == 100


def test_invalid_time_range():
    try:
        SearchRequest(
            location="Salem",
            date="2026-10-03",
            start_time="19:00",
            end_time="14:00",
            max_price=100,
        )
        assert False, "Expected validation error"
    except ValueError as error:
        assert "start_time must be earlier than end_time" in str(error)


def test_invalid_max_price():
    try:
        SearchRequest(
            location="Salem",
            date="2026-10-03",
            start_time="14:00",
            end_time="19:00",
            max_price=0,
        )
        assert False, "Expected validation error"
    except ValueError:
        pass
