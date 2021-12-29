import random
import string
from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import get_session
from controllers import parse, create_response_ok,\
  create_bulk_users, create_response_bad

from models import User, Token

user_router = APIRouter(prefix="/users",
    tags=["users"])


@user_router.post("/create_users/{quantity}", )
async def create_users(quantity: int, session: AsyncSession = Depends(get_session)):

    await create_bulk_users(quantity, session)
  
    return create_response_ok("Users created succesfully!")


@user_router.get("/get_user/{id}", )
async def create_users(id: int, session: AsyncSession = Depends(get_session)):

    user = await User.GetById(id, session)

    return create_response_ok(user)

@user_router.post("/login")
async def login(params: Dict[Any, Any], session: AsyncSession = Depends(get_session)):

    if "email" not in params:
        return create_response_bad("Email is required")
    if "password" not in params:
        return create_response_bad("Password is required")

    users = await User.GetByArgs({"email":params['email']}, session)
    if len(users) > 1:
        return create_response_bad("More than 1 user has the same email")

    user = users[0]

    if not user:
        return create_response_bad("User not found")
    else:
        args = {}
        args['email'] = params['email']
        args['password'] = params['password']
        token = await Token.Search(args, session)
        if token:
            return create_response_ok("User logged in!", token.to_dict())
        else:
            return create_response_bad("Password is not correct!")

@user_router.post("/sign-up")
async def sign_up(params: Dict[Any, Any], session: AsyncSession = Depends(get_session)):

    if "password" not in params:
        return create_response_bad("Password is not present")

    password = params.pop('password')
    
    try:
        await User.AddNew(params, session)
    except Exception as e:
         return create_response_bad(str(e))

    del params['username']
    params['password'] = password
    token = Token.AddNew(params, session)

    return create_response_ok("User created!", token.to_dict())

# small fix



    
















    

