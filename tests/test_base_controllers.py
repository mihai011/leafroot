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
async def test_greetings_controller():
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
async def test_initial_user_flow():
    """
    testing simple flow
    """

    user_signup_data = {
        "password": "test",
        "username": "control",
        "email": "test@gmail.com",
    }
    ds = DataSource()
    await ds.get_session()

    async with AsyncClient(app=app, base_url="http://test") as client:

        user_login_data = {"password": "test", "email": "test@gmail.com"}

        response = await client.post("users/login", json=user_login_data)
        assert response.status_code == 200
        assert response.json()["message"] == "User logged in!"
        item = response.json()["item"]
        token = item["token"]
        user_id = item["user"]["id"]
        headers = {"Authorization": "Bearer {}".format(token)}

        user_login_data = {"password": "test"}

        response = await client.post("users/login", json=user_login_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content['status'] == 400

        user_login_data = {"email": "test@gmail.com"}

        response = await client.post("users/login", json=user_login_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content['status'] == 400

        user_login_data = {"email": "no_such_user@gmail.com","password":"test"}

        response = await client.post("users/login", json=user_login_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content['status'] == 400

        user_login_data = {"email": "test@gmail.com", "password": "fake_test"}

        response = await client.post("users/login", json=user_login_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content['status'] == 400

        user_signup_data = {
            "username":"test",
            "email" : "test@gmail.com",
        }

        response = await client.post("users/sign-up", json=user_signup_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content['status'] == 400

        user_signup_data = {
            "username":"test",
            "password": "some_password"
        }

        response = await client.post("users/sign-up", json=user_signup_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content['status'] == 400

        user_signup_data = {
            "email" : "test@gmail.com",
            "password": "some_password"
        }

        response = await client.post("users/sign-up", json=user_signup_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content['status'] == 400

        user_signup_data = {
            "username": "test_duplicate",
            "email" : "test@gmail.com",
            "password": "some_password",
        }

        response = await client.post("users/sign-up", json=user_signup_data)
        response_content = response.json()
        assert response.status_code == 200
        assert response_content['status'] == 400

        response = await client.get(
            "/users/get_user/{}".format(user_id), headers=headers
        )
        assert response.status_code == 200

        response = await client.get(
            "/users/get_user/{}".format(3), headers=headers
        )
        assert response.status_code == 200
        response_content = response.json()
        assert response_content["status"] == 400

        response = await client.post(
            "/users/create_users/{}".format(2), headers=headers, json={}
        )
        assert response.status_code == 200


        # test with fake authorization headers
        fake_headers = {}
        fake_headers["Authorization"] = "Bearer fake"
        response = await client.get(
            "/users/get_user/{}".format(user_id), headers=fake_headers
        )
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 401

        # test endpoint for creating users
        response = await client.post(
            "/users/create_users/{}".format(100),
            headers=headers,
            json={"fake_content": "fake"},
        )
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        # test endpoint for creating users
        response = await client.post(
            "/users/create_user",
            headers=headers,
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
            headers=headers,
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
        response = await client.post("/users/create_user", headers=headers, json={})
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 400

        users = await User.GetAll(ds.session)
        assert len(users) == 117730
        await ds.close_session()
