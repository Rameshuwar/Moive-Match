from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    genre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    certification: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    release_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    poster_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    shows = relationship(
        "Show",
        back_populates="movie",
    )