from sqlalchemy import (
    JSON,
    VARCHAR,
    Column,
    Computed,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Users(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str]
    hashed_password :Mapped[str]

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self):
        return f'{self.email}'