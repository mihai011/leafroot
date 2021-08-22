from typing import Optional
from fastapi import FastAPI, APIRouter
from sqlalchemy.orm import session
from starlette.graphql import GraphQLApp
import graphene

from controllers.users_controllers import user_router

from models import QueryUser, User, session
from controllers.users_controllers import create_users

app = FastAPI()

general_router = APIRouter()

general_router.add_route("/graphql", \
    GraphQLApp(schema=graphene.Schema(query=QueryUser)))

app.include_router(user_router)