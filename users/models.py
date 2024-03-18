from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Date, Computed, VARCHAR
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class Users(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str]
    hashed_password :Mapped[str]