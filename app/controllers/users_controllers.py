import random
import string

from fastapi import APIRouter

from controllers import parse, create_response_ok,\
  create_bulk_users

from models import User

user_router = APIRouter(prefix="/users",
    tags=["users"])


@user_router.post("/create_users/{quantity}", )
async def create_users(quantity: int):

    await create_bulk_users(quantity)
  
    return create_response_ok("Users created succesfully!")


@user_router.get("/get_user/{id}", )
async def create_users(id: int):

    user = User.GetById(id)

    return create_response_ok(user)