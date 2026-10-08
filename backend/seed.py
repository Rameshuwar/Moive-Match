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
        # Prevent duplicate seed data.
        # If movie data already exists, the seed is skipped.
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

        # October 3
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

        # October 4
        show5 = Show(
            movie_id=movie1.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 4),
            show_time=time(11, 0),
        )

        show6 = Show(
            movie_id=movie2.id,
            screen_id=screen2.id,
            show_date=date(2026, 10, 4),
            show_time=time(13, 30),
        )

        show7 = Show(
            movie_id=movie3.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 4),
            show_time=time(18, 0),
        )

        show8 = Show(
            movie_id=movie1.id,
            screen_id=screen3.id,
            show_date=date(2026, 10, 4),
            show_time=time(20, 30),
        )

        # October 5
        show9 = Show(
            movie_id=movie2.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 5),
            show_time=time(10, 30),
        )

        show10 = Show(
            movie_id=movie3.id,
            screen_id=screen2.id,
            show_date=date(2026, 10, 5),
            show_time=time(15, 30),
        )

        show11 = Show(
            movie_id=movie1.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 5),
            show_time=time(18, 30),
        )

        show12 = Show(
            movie_id=movie2.id,
            screen_id=screen3.id,
            show_date=date(2026, 10, 5),
            show_time=time(21, 30),
        )

        # October 6
        show13 = Show(
            movie_id=movie3.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 6),
            show_time=time(11, 30),
        )

        show14 = Show(
            movie_id=movie1.id,
            screen_id=screen2.id,
            show_date=date(2026, 10, 6),
            show_time=time(14, 0),
        )

        show15 = Show(
            movie_id=movie2.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 6),
            show_time=time(17, 30),
        )

        show16 = Show(
            movie_id=movie3.id,
            screen_id=screen3.id,
            show_date=date(2026, 10, 6),
            show_time=time(22, 0),
        )

        # October 7
        show17 = Show(
            movie_id=movie1.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 7),
            show_time=time(9, 30),
        )

        show18 = Show(
            movie_id=movie2.id,
            screen_id=screen2.id,
            show_date=date(2026, 10, 7),
            show_time=time(13, 0),
        )

        show19 = Show(
            movie_id=movie3.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 7),
            show_time=time(19, 0),
        )

        show20 = Show(
            movie_id=movie1.id,
            screen_id=screen3.id,
            show_date=date(2026, 10, 7),
            show_time=time(21, 45),
        )

        # October 8
        show21 = Show(
            movie_id=movie2.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 8),
            show_time=time(10, 0),
        )

        show22 = Show(
            movie_id=movie3.id,
            screen_id=screen2.id,
            show_date=date(2026, 10, 8),
            show_time=time(14, 30),
        )

        show23 = Show(
            movie_id=movie1.id,
            screen_id=screen1.id,
            show_date=date(2026, 10, 8),
            show_time=time(18, 30),
        )

        show24 = Show(
            movie_id=movie2.id,
            screen_id=screen3.id,
            show_date=date(2026, 10, 8),
            show_time=time(21, 30),
        )

        shows = [
            show1,
            show2,
            show3,
            show4,
            show5,
            show6,
            show7,
            show8,
            show9,
            show10,
            show11,
            show12,
            show13,
            show14,
            show15,
            show16,
            show17,
            show18,
            show19,
            show20,
            show21,
            show22,
            show23,
            show24,
        ]

        db.add_all(shows)
        db.flush()

        # -------------------------
        # Prices / availability
        # -------------------------

        prices = [
            ShowPrice(
                show_id=show1.id,
                ticket_price=100,
                available_seats=18,
            ),
            ShowPrice(
                show_id=show2.id,
                ticket_price=90,
                available_seats=32,
            ),
            ShowPrice(
                show_id=show3.id,
                ticket_price=150,
                available_seats=20,
            ),
            ShowPrice(
                show_id=show4.id,
                ticket_price=120,
                available_seats=25,
            ),
            ShowPrice(
                show_id=show5.id,
                ticket_price=110,
                available_seats=40,
            ),
            ShowPrice(
                show_id=show6.id,
                ticket_price=140,
                available_seats=28,
            ),
            ShowPrice(
                show_id=show7.id,
                ticket_price=180,
                available_seats=16,
            ),
            ShowPrice(
                show_id=show8.id,
                ticket_price=200,
                available_seats=12,
            ),
            ShowPrice(
                show_id=show9.id,
                ticket_price=90,
                available_seats=35,
            ),
            ShowPrice(
                show_id=show10.id,
                ticket_price=150,
                available_seats=22,
            ),
            ShowPrice(
                show_id=show11.id,
                ticket_price=180,
                available_seats=14,
            ),
            ShowPrice(
                show_id=show12.id,
                ticket_price=220,
                available_seats=10,
            ),
            ShowPrice(
                show_id=show13.id,
                ticket_price=100,
                available_seats=30,
            ),
            ShowPrice(
                show_id=show14.id,
                ticket_price=130,
                available_seats=24,
            ),
            ShowPrice(
                show_id=show15.id,
                ticket_price=170,
                available_seats=18,
            ),
            ShowPrice(
                show_id=show16.id,
                ticket_price=250,
                available_seats=8,
            ),
            ShowPrice(
                show_id=show17.id,
                ticket_price=90,
                available_seats=42,
            ),
            ShowPrice(
                show_id=show18.id,
                ticket_price=140,
                available_seats=26,
            ),
            ShowPrice(
                show_id=show19.id,
                ticket_price=190,
                available_seats=15,
            ),
            ShowPrice(
                show_id=show20.id,
                ticket_price=230,
                available_seats=9,
            ),
            ShowPrice(
                show_id=show21.id,
                ticket_price=100,
                available_seats=38,
            ),
            ShowPrice(
                show_id=show22.id,
                ticket_price=150,
                available_seats=21,
            ),
            ShowPrice(
                show_id=show23.id,
                ticket_price=180,
                available_seats=17,
            ),
            ShowPrice(
                show_id=show24.id,
                ticket_price=210,
                available_seats=11,
            ),
        ]

        db.add_all(prices)

        db.commit()

        print("MovieMatch development data seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
