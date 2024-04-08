"""Diagram for photo store"""

# FastApi, Postgresql, Redis, Minio(S3)
from diagrams import Diagram
from diagrams import Diagram

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

    user >> api >> minio
    api >> postgres
    api >> redis
