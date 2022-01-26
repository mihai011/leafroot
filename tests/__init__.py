from fastapi import Depends
from fastapi.testclient import TestClient

from app.app import app
from data.models import get_session
from data.models.user import User

client = TestClient(app)



class DataSource():

    def __init__(self, session = Depends(get_session)):

        self.session = session
        self.client = client
        args = {"username":"Test_user", \
            "email":"test@gmail.com", \
            "password":"test"}

        response = client.post("users/sign-up", json=args)
        assert response['status'] == 200

        args={
            "username":"Test_user",
            "password": "test"
        }

        response = client.post('/users/login', json=args)

        self.headers = {"Authorization":"Bearer {}".format(response['item']['token'])}
        
