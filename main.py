from dataclasses import dataclass
from datetime import date
from typing import Annotated, Optional

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_bookings)


# class HotelsSearchArgs:
#     def __init__(self,
#                  location: str,
#                  date_from: date,
#                  date_to: date,
#                  has_spa: bool = None,
#                  stars: Annotated[int, Query(ge=1, le=5)] = None,
#                  ):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.has_spa = has_spa
#         self.stars = stars
######=============#########
@dataclass
class HotelsSearchArgs():
    location: str
    date_from: date
    date_to: date
    has_spa: bool = None
    stars: Annotated[int, Query(ge=1, le=5)] = None


@app.get('/hotels')
async def get_hotels(
    search_args : HotelsSearchArgs = Depends()
):

    return search_args



class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post('/bookings')
def add_booking(booking: SBooking):
    pass