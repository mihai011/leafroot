from typing import Optional
from fastapi import FastAPI
from sqlalchemy.orm import session
from starlette.graphql import GraphQLApp
import graphene

from models import QueryUser, User, session

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/create_users/{quantity}")
def create_users(quantity: int):

    user_args = {
        "email": "email@test.com",
        "verified": True,
        "username": "control"
    }

    for i in range(quantity):

        args = {}
        args['email'] = user_args['email'] + str(i)
        args['username'] = user_args['username'] + str(i) 
        args['verified'] = user_args['verified']

        User.AddNew(args)

app.add_route("/graphql", \
    GraphQLApp(schema=graphene.Schema(query=QueryUser)))