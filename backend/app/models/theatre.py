from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Theatre(Base):
    __tablename__ = "theatres"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    district: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    screens = relationship(
        "Screen",
        back_populates="theatre",
        cascade="all, delete-orphan",
    )