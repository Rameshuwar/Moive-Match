from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Screen(Base):
    __tablename__ = "screens"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    theatre_id: Mapped[int] = mapped_column(
        ForeignKey("theatres.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    theatre = relationship(
        "Theatre",
        back_populates="screens",
    )

    shows = relationship(
        "Show",
        back_populates="screen",
        cascade="all, delete-orphan",
    )