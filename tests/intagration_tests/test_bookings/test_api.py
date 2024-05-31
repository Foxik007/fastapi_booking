import pytest
from httpx import AsyncClient
from sqlalchemy import delete

from bookings.dao import BookingDAO
from bookings.models import Bookings
from database import Base, engine


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    (4, "2030-05-01", "2030-05-15", 3, 200),
    (4, "2030-05-02", "2030-05-16", 4, 200),
    (4, "2030-05-03", "2030-05-17", 5, 200),
    (4, "2030-05-04", "2030-05-18", 6, 200),
    (4, "2030-05-05", "2030-05-19", 7, 200),
    (4, "2030-05-06", "2030-05-20", 8, 200),
    (4, "2030-05-07", "2030-05-21", 9, 200),
    (4, "2030-05-08", "2030-05-22", 10,200),
    (4, "2030-05-09", "2030-05-23", 10,401),
    (4, "2030-05-10", "2030-05-24", 10, 401),
    ])
async def test_add_and_get_booking(
        room_id,
        date_from,
        date_to,
        booked_rooms,
        status_code,
        authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post("/bookings/add", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code




