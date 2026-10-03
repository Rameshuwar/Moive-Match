from datetime import date, time

from app.db.database import SessionLocal
from app.models.movie import Movie
from app.models.theatre import Theatre
from app.models.screen import Screen
from app.models.show import Show
from app.models.show_price import ShowPrice


def seed_database():
    db = SessionLocal()

    try:
        # Prevent duplicate seed data
        if db.query(Movie).first():
            print("Database already contains movie data. Seed skipped.")
            return

        # -------------------------
        # Movies
        # -------------------------
        movie1 = Movie(
            title="Coolie",
            language="Tamil",
            duration_minutes=169,
            genre="Action",
            certification="UA",
            release_date=date(2025, 8, 14),
            poster_url=None,
        )

        movie2 = Movie(
            title="Dragon",
            language="Tamil",
            duration_minutes=157,
            genre="Comedy",
            certification="U",
            release_date=date(2025, 2, 21),
            poster_url=None,
        )

        movie3 = Movie(
            title="Retro",
            language="Tamil",
            duration_minutes=162,
            genre="Action",
            certification="UA",
            release_date=date(2025, 5, 1),
            poster_url=None,
        )

        db.add_all([movie1, movie2, movie3])
        db.flush()

        # -------------------------
        # Theatres
        # -------------------------
        theatre1 = Theatre(
            name="ARRS Multiplex",
            address="Salem, Tamil Nadu",
            district="Salem",
        )

        theatre2 = Theatre(
            name="Kailash Priksaa",
            address="Salem, Tamil Nadu",
            district="Salem",
        )

        db.add_all([theatre1, theatre2])
        db.flush()

        # -------------------------
        # Screens
        # -------------------------
        screen1 = Screen(
            theatre_id=theatre1.id,
            name="Screen 1",
        )

        screen2 = Screen(
            theatre_id=theatre1.id,
            name="Screen 2",
        )

        screen3 = Screen(
            theatre_id=theatre2.id,
            name="Screen 1",
        )

        db.add_all([screen1, screen2, screen3])
        db.flush()

        # -------------------------
        # Shows
        # -------------------------
        show1 = Show(
            movie_id=movie1.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 3),
            show_time=time(14, 30),
        )

        show2 = Show(
            movie_id=movie2.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 3),
            show_time=time(15, 0),
        )

        show3 = Show(
            movie_id=movie3.id,
            screen_id=screen2.id,
            show_date=date(2026, 10, 3),
            show_time=time(18, 30),
        )

        show4 = Show(
            movie_id=movie1.id,
            screen_id=screen3.id,
            show_date=date(2026, 10, 3),
            show_time=time(16, 0),
        )

        db.add_all([show1, show2, show3, show4])
        db.flush()

        # -------------------------
        # Prices / availability
        # -------------------------
        price1 = ShowPrice(
            show_id=show1.id,
            ticket_price=100,
            available_seats=18,
        )

        price2 = ShowPrice(
            show_id=show2.id,
            ticket_price=90,
            available_seats=32,
        )

        price3 = ShowPrice(
            show_id=show3.id,
            ticket_price=150,
            available_seats=20,
        )

        price4 = ShowPrice(
            show_id=show4.id,
            ticket_price=120,
            available_seats=25,
        )

        db.add_all([price1, price2, price3, price4])

        db.commit()

        print("MovieMatch development data seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
