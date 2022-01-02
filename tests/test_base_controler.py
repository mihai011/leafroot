import pytest
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncConnection
from controllers import users_controllers
from httpx import AsyncClient

from data.models import get_session_simple
from data  import User, Token
from app.app import app

from tests import client

def test_greetings_controller():

  response = client.get("/")
  assert response.status_code == 200
  assert response.json()['message'] == "Hello World"

@pytest.mark.asyncio
async def test_initial_user_flow():

  session  = await get_session_simple()

  await User.DeleteAll(session)
  await Token.DeleteAll(session)

  user_signup_data = {"password":"test", \
    "username":"control", \
    "email":"test@gmail.com"}

  async with AsyncClient(app=app, base_url="http://test") as client:
    response = await client.post("users/sign-up", json=user_signup_data)

    assert response.status_code == 200
    assert response.json()["message"] == "User created!"

    user_login_data= {"password":"test", \
      "email":"test@gmail.com"}

    response = await client.post("users/login", json=user_login_data)
    assert response.status_code == 200
    assert response.json()['message'] == "User logged in!"
    item = response.json()['item']
    token = item['token']
    user_id = item['user']['id']
    headers = {"Authorization":"Bearer {}".format(token)}

    response = await client.get("/users/get_user/{}".format(user_id), headers=headers)
    assert response.status_code == 200

    response = await client.post("/users/create_users/{}".format(2), headers=headers)
    assert response.status_code == 200

    

