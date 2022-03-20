"""
base module for testing
"""
import pytest

import nest_asyncio
from data import User
from tests import DataSource
from tests.conftest import temp_db

nest_asyncio.apply()


@pytest.mark.asyncio
@temp_db
async def test_greetings_controller(session):
    """
    testing simple controller
    """

    ds = DataSource()
    await ds.make_user()

    response = await ds.client.get("/", headers=ds.headers["Test_user"])
    assert response.status_code == 200
    assert response.json()["message"] == "Hello World"


@pytest.mark.asyncio
@temp_db
async def test_login_user(session):
    """
    testing simple flow
    """

    ds = DataSource()
    await ds.make_user({"email": "test@gmail.com"})
    user_login_data = {"password": "test"}

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400
    assert response_content["message"] == "Email is required"

    user_login_data = {"email": "test@gmail.com"}

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400
    assert response_content["message"] == "Password is required"

    user_login_data = {"email": "no_such_user@gmail.com", "password": "test"}

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400
    assert response_content["message"] == "No user with such email found"

    user_login_data = {"email": "test@gmail.com", "password": "fake_test"}

    response = await ds.client.post("users/login", json=user_login_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400
    assert response_content["message"] == "Incorrect password!"


@pytest.mark.asyncio
@temp_db
async def test_signup_user(session):
    """
    testing simple flow
    """

    ds = DataSource()
    await ds.make_user()
    user_signup_data = {"username": "test"}

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400

    user_signup_data = {"username": "test", "password": "some_password"}

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400

    user_signup_data = {"email": "test@gmail.com", "password": "some_password"}

    response = await ds.client.post("users/sign-up", json=user_signup_data)
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400

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

    # test with fake authorization headers
    fake_headers = {}
    fake_headers["Authorization"] = "Bearer fake"
    response = await ds.client.get(
        "/users/get_user/{}".format(user_id), headers=fake_headers
    )
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 401


@pytest.mark.asyncio
@temp_db
async def test_create_user(session):
    """
    testing simple flow
    """
    ds = DataSource()
    await ds.make_user()

    # test endpoint for creating users
    response = await ds.client.post(
        "/users/create_users/{}".format(100),
        headers=ds.headers["Test_user"],
        json={"fake_content": "fake"},
    )
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400

    response = await ds.client.post(
        "/users/create_users/{}".format(2), headers=ds.headers["Test_user"], json={}
    )
    assert response.status_code == 200

    # test endpoint for creating users
    response = await ds.client.post(
        "/users/create_user",
        headers=ds.headers["Test_user"],
        json={
            "username": "user_test",
            "email": "email@gmail.com",
            "hashed_pass": "hashed pass",
        },
    )
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 200

    # test endpoint for creating users (duplicate)
    response = await ds.client.post(
        "/users/create_user",
        headers=ds.headers["Test_user"],
        json={
            "username": "user_test",
            "email": "email@gmail.com",
            "hashed_pass": "hashed pass",
        },
    )
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400

    # test endpoint for creating users
    response = await ds.client.post(
        "/users/create_user", headers=ds.headers["Test_user"], json={}
    )
    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == 400

    users = await User.GetAll(session)
    assert len(users) == 4

    await User.DeleteAll(session)
    users = await User.GetAll(session)
    assert len(users) == 0
