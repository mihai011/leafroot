"""Base module for testing."""
import pytest

from data import User
from tests import DataSource


@pytest.mark.asyncio
async def test_greetings_controller(async_session):
    """Testing simple controller."""

    ds = DataSource(async_session)
    await ds.make_user()

    response = await ds.client.get("/", headers=ds.headers["Test_user"])
    assert response.status_code == 200
    assert "<html>" in response.text


@pytest.mark.asyncio
async def test_login_user(async_session):
    """Testing simple flow."""

    ds = DataSource(async_session)
    await ds.make_user({"email": "test@gmail.com"})
    user_login_data = {"password": "test"}

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400
    assert (
        response_content["message"]
        == "No user with such email or username found"
    )

    user_login_data = {"email": "test@gmail.com"}

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == 422

    user_login_data = {"email": "no_such_user@gmail.com", "password": "test"}

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400
    assert (
        response_content["message"]
        == "No user with such email or username found"
    )

    user_login_data = {"email": "test@gmail.com", "password": "fake_pass"}

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400
    assert response_content["message"] == "Incorrect password!"


@pytest.mark.asyncio
async def test_signup_user(async_session):
    """Testing simple flow."""

    ds = DataSource(async_session)
    await ds.make_user()
    user_signup_data = {"username": "test"}

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    response_content = response.json()
    assert response.status_code == 422

    user_signup_data = {"username": "test", "password": "some_password"}

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    response_content = response.json()
    assert response.status_code == 422

    user_signup_data = {"email": "test@gmail.com", "password": "some_password"}

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    response_content = response.json()
    assert response.status_code == 422

    user_signup_data = {
        "username": "test_duplicate",
        "email": "test_alternate@gmail.com",
        "password": "some_password",
    }

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 200

    user_signup_data = {
        "username": "test_duplicate",
        "email": "test_alternate@gmail.com",
        "password": "some_password",
    }

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400

    user_id = 2
    response = await ds.client.get(
        "/users/get_user/{}".format(user_id), headers=ds.headers["Test_user"]
    )
    assert response.status_code == 200

    user_id = 3
    response = await ds.client.get(
        "/users/get_user/{}".format(3), headers=ds.headers["Test_user"]
    )
    assert response.status_code == 200
    response_content = response.json()
    assert response_content["status"] == 400
    assert response_content["message"] == "User not found!"

    # test with fake authorization headers
    fake_headers = {}
    fake_headers["Authorization"] = "Bearer fake"
    response = await ds.client.get(
        "/users/get_user/{}".format(user_id), headers=fake_headers
    )
    response_content = response.json()
    assert response.status_code == 400
    assert response_content["detail"] == "(400, 'Not enough segments')"

    # test with no correct header
    fake_headers = {}
    fake_headers["header"] = "Bearer fake"
    response = await ds.client.get(
        "/users/get_user/{}".format(user_id), headers=fake_headers
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user(async_session):
    """Testing simple flow."""
    ds = DataSource(async_session)
    await ds.make_user()

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
    response_content = response.json()
    assert response_content["status"] == 200

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
    response_content = response.json()
    assert response.status_code == 422

    # test endpoint for creating users
    response = await ds.client.post(
        "/users/create_user", headers=ds.headers["Test_user"], json={}
    )
    response_content = response.json()
    assert response.status_code == 422

    users = await User.GetAll(async_session)
    assert len(users) == 2

    await User.DeleteAll(async_session)
    users = await User.GetAll(async_session)
    assert len(users) == 0
