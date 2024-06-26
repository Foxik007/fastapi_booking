import pytest

from users.dao import UsersDAO


@pytest.mark.parametrize('user_id,email,is_exists',[
    (1,'test@test.com',True),
    (2,'artem@example.com',True),
    (3,'asdsadas@mail.ru',False),
])
async def test_find_user_by_id(user_id,email,is_exists):
    user = await UsersDAO.find_by_id(user_id)
    if is_exists:
        assert user
        assert user.id == user_id
        assert user.email == email

    else:
        not user