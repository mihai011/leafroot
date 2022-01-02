from starlette.graphql import GraphQLApp
import graphene
import time

from fastapi import FastAPI, APIRouter, Request

from controllers.users_controllers import user_router
from controllers.base_controllers import base_router
from controllers.atom_controllers import atom_router
from data import QueryUser

app = FastAPI()

general_router = APIRouter()

general_router.add_route("/graphql", \
    GraphQLApp(schema=graphene.Schema(query=QueryUser)))

app.include_router(user_router)
app.include_router(atom_router)
app.include_router(base_router)

@app.middleware("http")
async def add_time_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
