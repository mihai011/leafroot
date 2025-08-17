"""Base module for testing."""

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from data import User
from tests import DataSource

STATUS_CODE_200 = status.HTTP_200_OK


async def test_greetings_controller(async_session: AsyncSession) -> None:
    """Testing simple controller."""
    ds = DataSource(async_session)
    await ds.make_user()

    response = await ds.client.get("/", headers=ds.headers["Test_user"])
    assert response.status_code == STATUS_CODE_200
    assert '<html lang="en">' in response.text


async def test_login_user(async_session: AsyncSession) -> None:
    """Testing simple flow."""
    ds = DataSource(async_session)
    data_login = {"email": "test@gmail.com", "password": "test"}
    await ds.make_user(data_login)
    unknown_data_login = {
        "email": "test2@gmail.com",
        "password": "test2",
        "username": "test2",
    }

    response = await ds.client.post("users/login", json=unknown_data_login)
    response_content = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_content["detail"] == "No user with such email or username found!"

    user_login_data = {"email": "test@gmail.com", "password": "test"}

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "username" in response_content["detail"][0]["loc"]
    assert response_content["detail"][0]["msg"] == "Field required"

    user_login_data = {
        "email": "no_such_user@gmail.com",
        "password": "test",
        "username": "test",
    }

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_content["detail"] == "No user with such email or username found!"

    user_login_data = {
        "email": "test@gmail.com",
        "password": "fake_pass",
        "username": "Test_user",
    }

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_content["detail"] == "Incorrect Password!"


async def test_signup_user(async_session: AsyncSession) -> None:
    """Testing simple flow."""
    ds = DataSource(async_session)
    await ds.make_user()
    user_signup_data = {"username": "test"}

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    user_signup_data = {"username": "test", "password": "some_password"}

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    user_signup_data = {"email": "test@gmail.com", "password": "some_password"}

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    user_signup_data = {
        "username": "test_duplicate",
        "email": "test_alternate@gmail.com",
        "password": "some_password",
        "permissions": "110",
    }

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    user_id = 2
    response = await ds.client.get(
        f"/users/get_user/{user_id}",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK

    user_id = 3
    response = await ds.client.get(
        f"/users/get_user/{user_id}",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK
    response_content = response.json()
    assert response_content["detail"] == "No user found!"

    # test with fake authorization headers
    fake_headers = {}
    fake_headers["Authorization"] = "Bearer fake"
    response = await ds.client.get(
        f"/users/get_user/{user_id}",
        headers=fake_headers,
    )
    response_content = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_content["detail"] == "Invalid token!"

    # test with no correct header
    fake_headers = {}
    fake_headers["header"] = "Bearer fake"
    response = await ds.client.get(
        f"/users/get_user/{user_id}",
        headers=fake_headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_user(async_session: AsyncSession) -> None:
    """Testing simple flow."""
    ds = DataSource(async_session)
    await ds.make_user()

    total_users = 2
    left_users = 0

    # test endpoint for creating user
    response = await ds.client.post(
        "/users/create_user",
        headers=ds.headers["Test_user"],
        json={
            "username": "user_test",
            "email": "email@gmail.com",
            "password": "hashed pass",
        },
    )
    assert response.status_code == status.HTTP_200_OK

    # test endpoint for creating users (duplicate)
    response = await ds.client.post(
        "/users/create_user",
        headers=ds.headers["Test_user"],
        json={
            "username": "user_test",
            "email": "email@gmail.com",
            "pass": "hashed pass",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # test endpoint for creating users
    response = await ds.client.post(
        "/users/create_user",
        headers=ds.headers["Test_user"],
        json={},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    users = await User.get_all(async_session)
    assert len(users) == total_users

    await User.delete_all(async_session)
    users = await User.get_all(async_session)
    assert len(users) == left_users
