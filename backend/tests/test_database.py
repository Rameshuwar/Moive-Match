from sqlalchemy import text


def test_database_connection(db):
    result = db.execute(text("SELECT current_database()")).scalar_one()

    assert result == "moviematch_test"


def test_movie_duration_must_be_positive(db):
    from app.models import Movie
    from sqlalchemy.exc import IntegrityError

    movie = Movie(
        title="Invalid Movie",
        language="Tamil",
        duration_minutes=0,
        genre="Action",
        certification="U",
        release_date="2026-01-01",
    )

    db.add(movie)

    try:
        db.commit()
        assert False, "Expected IntegrityError"
    except IntegrityError:
        db.rollback()


def test_ticket_price_must_be_positive(db):
    from app.models import ShowPrice
    from sqlalchemy.exc import IntegrityError

    show_id = db.execute(
        ShowPrice.__table__.select()
    ).first().show_id

    price = ShowPrice(
        show_id=show_id,
        ticket_price=0,
        available_seats=10,
    )

    db.add(price)

    try:
        db.commit()
        assert False, "Expected IntegrityError"
    except IntegrityError:
        db.rollback()


def test_available_seats_cannot_be_negative(db):
    from app.models import ShowPrice
    from sqlalchemy.exc import IntegrityError

    show_id = db.execute(
        ShowPrice.__table__.select()
    ).first().show_id

    price = ShowPrice(
        show_id=show_id,
        ticket_price=100,
        available_seats=-1,
    )

    db.add(price)

    try:
        db.commit()
        assert False, "Expected IntegrityError"
    except IntegrityError:
        db.rollback()
