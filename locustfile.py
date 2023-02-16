"""Some docstring."""

from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def login(self):
        self.client.post(
            "https://860d-18-185-106-164.eu.ngrok.io/users/login",
            json={
                "email": "admin@email.com",
                "password": "pass",
            },
        )
