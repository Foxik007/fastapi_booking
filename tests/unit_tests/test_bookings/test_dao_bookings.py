from httpx import AsyncClient

from bookings.dao import BookingDAO


async def test_delete_and_get_booking(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get('/bookings')
    a = response.json()
    x = a[0]['user_id']
    await BookingDAO.delete(user_id=x)
    assert await BookingDAO.find_all(user_id=x) == []