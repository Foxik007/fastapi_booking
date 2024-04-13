from typing import Optional

from pydantic import BaseModel, ConfigDict


class SHotels(BaseModel):
    id: int
    name: int
    location: int
    services: Optional[list[str]]
    rooms_quantity: int
    image_id : int

    model_config = ConfigDict(from_attributes=True)