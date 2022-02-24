"""
base module for testing
"""
import pytest
from httpx import AsyncClient

import nest_asyncio
from app.app import app
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

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/", headers=ds.headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Hello World"


@pytest.mark.asyncio
@temp_db
async def test_login_user(session):
    """
    testing simple flow
    """

    ds = DataSource()

    async with AsyncClient(app=app, base_url="http://test") as client:

        user_login_data = {"password": "test", "email": "test@gmail.com"}

        user_login_data = {"password": "test"}

        response = await client.post("users/login", json=user_login_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        user_login_data = {"email": "test@gmail.com"}

        response = await client.post("users/login", json=user_login_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        user_login_data = {"email": "no_such_user@gmail.com", "password": "test"}

        response = await client.post("users/login", json=user_login_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        user_login_data = {"email": "test@gmail.com", "password": "fake_test"}

        response = await client.post("users/login", json=user_login_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400


@pytest.mark.asyncio
@temp_db
async def test_signup_user(session):
    """
    testing simple flow
    """

    
    ds = DataSource()

    async with AsyncClient(app=app, base_url="http://test") as client:

        user_signup_data = {"username": "test"}

        response = await client.post("users/sign-up", json=user_signup_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        user_signup_data = {"username": "test", "password": "some_password"}

        response = await client.post("users/sign-up", json=user_signup_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        user_signup_data = {"email": "test@gmail.com", "password": "some_password"}

        response = await client.post("users/sign-up", json=user_signup_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        user_signup_data = {
            "username": "test_duplicate",
            "email": "test@gmail.com",
            "password": "some_password",
        }

        response = await client.post("users/sign-up", json=user_signup_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        user_id = 1
        response = await client.get("/users/get_user/{}".format(1), headers=ds.headers)
        assert response.status_code == 200

        response = await client.get("/users/get_user/{}".format(3), headers=ds.headers)
        assert response.status_code == 200
        response_content = response.json()
        assert response_content["status"] == 400

        # test with fake authorization headers
        fake_headers = {}
        fake_headers["Authorization"] = "Bearer fake"
        response = await client.get(
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

    async with AsyncClient(app=app, base_url="http://test") as client:

        # test endpoint for creating users
        response = await client.post(
            "/users/create_users/{}".format(100),
            headers=ds.headers,
            json={"fake_content": "fake"},
        )
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        response = await client.post(
            "/users/create_users/{}".format(2), headers=ds.headers, json={}
        )
        assert response.status_code == 200

        # test endpoint for creating users
        response = await client.post(
            "/users/create_user",
            headers=ds.headers,
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
        response = await client.post(
            "/users/create_user",
            headers=ds.headers,
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
        response = await client.post("/users/create_user", headers=ds.headers, json={})
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        users = await User.GetAll(session)
        assert len(users) == 4

        await User.DeleteAll(session)
        users = await User.GetAll(session)
        assert len(users) == 0

        
