from datetime import date, time

from sqlalchemy import Date, ForeignKey, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Show(Base):
    __tablename__ = "shows"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id"),
        nullable=False,
        index=True,
    )

    screen_id: Mapped[int] = mapped_column(
        ForeignKey("screens.id"),
        nullable=False,
        index=True,
    )

    show_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    show_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    movie = relationship(
        "Movie",
        back_populates="shows",
    )

    screen = relationship(
        "Screen",
        back_populates="shows",
    )

    prices = relationship(
        "ShowPrice",
        back_populates="show",
        cascade="all, delete-orphan",
    )