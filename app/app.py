from typing import Optional
from fastapi import FastAPI, APIRouter
from sqlalchemy.orm import session
from starlette.graphql import GraphQLApp
import graphene

from models import QueryUser, User, session
from controllers.users_controllers import create_users

app = FastAPI()
router = APIRouter()



@router.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


router.add_route("/create_users/{quantity}", create_users, ["POST"])
router.add_route("/graphql", \
    GraphQLApp(schema=graphene.Schema(query=QueryUser)))

app.include_router(router)