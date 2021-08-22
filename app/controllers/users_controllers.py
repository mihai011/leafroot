import random
import string
from typing import Any, Dict

from fastapi import APIRouter, Request

from controllers import parse, create_response_ok,\
  create_bulk_users, create_response_bad

from models import User, Token

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

@user_router.post("/login")
def login(params: Dict[Any, Any]):

    if "email" not in params:
        return create_response_bad("Email is required")
    if "password" not in params:
        return create_response_bad("Password is required")

    users = User.GetByArgs({"email":params['email']})
    if len(users) > 1:
        return create_response_bad("More than 1 user has the same email")

    user = users[0]

    if not user:
        return create_response_bad("User not found")
    else:
        args = {}
        args['email'] = params['email']
        args['password'] = params['password']
        token = Token.Search(args)
        if token:
            return create_response_ok("User logged in!", token.to_dict())
        else:
            return create_response_bad("Password is not correct!")

@user_router.post("/sign-up")
def sign_up(params: Dict[Any, Any]):

    if "password" not in params:
        return create_response_bad("Password is not present")

    password = params.pop('password')
    
    try:
        User.AddNew(params)
    except Exception as e:
         return create_response_bad(str(e))

    del params['username']
    params['password'] = password
    token = Token.AddNew(params)

    return create_response_ok("User created!", token.to_dict() )



    
















    

