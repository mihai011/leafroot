"""Some docstring."""

from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def login(self):
        self.client.post(
            "https://181b-3-68-197-147.eu.ngrok.io/users/login",
            json={
                "email": "admin@email.com",
                "password": "pass",
            },
        )
