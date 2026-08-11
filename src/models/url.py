from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Url(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(primary_key=True)
    full: Mapped[str] = mapped_column(String(256))
    short: Mapped[str] = mapped_column(String(8))
    creation_date: Mapped[date] = mapped_column(Date)
    expiration_date: Mapped[date] = mapped_column(Date)