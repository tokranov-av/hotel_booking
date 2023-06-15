import pytest

from app.users.dao import UserDAO

users_data = (
    ('test@test.com', True),
    ('artur@example.com', True),
    ('...', False)
)


@pytest.mark.parametrize('email, is_exist',  users_data)
async def test_user_find_one_or_none(email, is_exist):
    user = await UserDAO.find_one_or_none(email=email)

    if is_exist:
        assert user
        assert user.get('email') == email
    else:
        assert not user
