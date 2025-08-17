"""Diagram for photo store."""

from diagrams import Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import Fastapi

with Diagram("Photo Store", show=False):
    user = User("User")
    api = Fastapi("FastApi")
    redis = Redis("Redis")
    postgres = Postgresql("Postgresql")
    minio = Custom("Minio", "minio-logo-white.png")

    user >> Edge() << api
    api >> Edge() << postgres
    api >> Edge() << redis
    api >> Edge() << minio
