from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ShowPrice(Base):
    __tablename__ = "show_prices"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    show_id: Mapped[int] = mapped_column(
        ForeignKey("shows.id"),
        nullable=False,
        index=True,
    )

    ticket_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    available_seats: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    show = relationship(
        "Show",
        back_populates="prices",
    )