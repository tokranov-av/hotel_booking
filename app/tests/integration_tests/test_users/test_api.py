import pytest
from httpx import AsyncClient

from app.users.router import router_auth


register_user_data = (
    ('kot@pes.com', 'kotopes', 201),
    ('kot@pes.com', 'kot0pes', 409),
    ('pes@kot.com', 'pesokot', 201),
    ('abcde', 'pesokot', 422)
)


@pytest.mark.parametrize('email, password, status_code', register_user_data)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        router_auth.url_path_for('register_user'),
        json={'email': email, 'password': password}
    )
    assert response.status_code == status_code


login_user_data = (
    ('test@test.com', 'test', 200),
    ('artur@example.com', 'artur', 200),
    ('does_not_exist_user@example.com', 'not_exist', 401),
)


@pytest.mark.parametrize('email, password, status_code', login_user_data)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        router_auth.url_path_for('login_user'),
        json={'email': email, 'password': password}
    )
    assert response.status_code == status_code
