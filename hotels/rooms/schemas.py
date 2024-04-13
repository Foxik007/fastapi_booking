from typing import Optional

from pydantic import BaseModel, ConfigDict


class sAvailableRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: Optional[list[str]]
    quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)