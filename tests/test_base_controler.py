from tests import client

def test_greetings_controller():

  response = client.get("/")
  assert response.status_code == 200
  assert response.json()['message'] == "Hello World"

def test_initial_flow():

  user_signup_data = {"password":"test", \
    "username":"control", \
    "email":"test@gmail.com"}
  response = client.post("/users/sign-up", json=user_signup_data)
  assert response.status_code == 200
  assert response.json()["message"] == "User created!"