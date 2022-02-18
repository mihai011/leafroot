"""
base module for testing
"""
import pytest
from httpx import AsyncClient

import nest_asyncio
from app.app import app
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

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("users/sign-up", json=user_signup_data)

        assert response.status_code == 200
        assert response.json()["message"] == "User created!"

        user_login_data = {"password": "test", "email": "test@gmail.com"}

        response = await client.post("users/login", json=user_login_data)
        assert response.status_code == 200
        assert response.json()["message"] == "User logged in!"
        item = response.json()["item"]
        token = item["token"]
        user_id = item["user"]["id"]
        headers = {"Authorization": "Bearer {}".format(token)}

        response = await client.get(
            "/users/get_user/{}".format(user_id), headers=headers
        )
        assert response.status_code == 200

        response = await client.post(
            "/users/create_users/{}".format(2), headers=headers, json={}
        )
        assert response.status_code == 200

        # test with fake authorization headers
        headers["Authorization"] = "Bearer fake"
        response = await client.get(
            "/users/get_user/{}".format(user_id), headers=headers
        )
        response_content = response.json()
        assert response.status_code == 200
        assert response_content["status"] == 401
