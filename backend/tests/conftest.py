import os
from datetime import date, time

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Movie, Theatre, Screen, Show, ShowPrice


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not set")

test_database_url = database_url.rsplit("/", 1)[0] + "/moviematch_test"

test_engine = create_engine(
    test_database_url,
    pool_pre_ping=True,
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture
def db():
    session = TestSessionLocal()

    try:
        movie = Movie(
            title="Test Movie",
            language="Tamil",
            duration_minutes=150,
            genre="Action",
            certification="U",
            release_date=date(2026, 1, 1),
        )

        theatre = Theatre(
            name="Test Theatre",
            address="Test Address",
            district="Salem",
        )

        session.add_all([movie, theatre])
        session.flush()

        screen = Screen(
            theatre_id=theatre.id,
            name="Screen 1",
        )

        session.add(screen)
        session.flush()

        show = Show(
            movie_id=movie.id,
            screen_id=screen.id,
            show_date=date(2026, 10, 3),
            show_time=time(15, 0),
        )

        session.add(show)
        session.flush()

        show_price = ShowPrice(
            show_id=show.id,
            ticket_price=90,
            available_seats=32,
        )

        session.add(show_price)
        session.commit()

        yield session

    finally:
        session.rollback()
        session.query(ShowPrice).delete()
        session.query(Show).delete()
        session.query(Screen).delete()
        session.query(Movie).delete()
        session.query(Theatre).delete()
        session.commit()
        session.close()
