from sqlalchemy import Date
from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"
    player_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(nullable=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    team: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    squad: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[str] = mapped_column(nullable=False)


