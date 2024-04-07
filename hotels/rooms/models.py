from typing import Optional

from sqlalchemy import Column,VARCHAR, Integer, String, JSON, ForeignKey, Date, Computed
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Rooms(Base):
    __tablename__ = 'rooms'

    id : Mapped[int] = mapped_column(primary_key=True)
    hotel_id : Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str]
    description : Mapped[str]
    price : Mapped[int]
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]
