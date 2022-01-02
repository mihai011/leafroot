from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import get_session
from controllers import create_response_ok,\
  create_bulk_users, create_response_bad
from utils import create_access_token, get_password_hash,\
    verify_password, oauth2_scheme, authenthicate_user

from data import User

user_router = APIRouter(prefix="/users",
    tags=["users"])


@user_router.post("/create_users/{quantity}", )
async def create_users(quantity: int, session: AsyncSession = Depends(get_session),\
    token: str = Depends(oauth2_scheme)):

    if not await authenthicate_user(token, session):
        return create_response_bad("Token expired! Please login again!")

    await create_bulk_users(quantity, session)
    await session.close()
    return create_response_ok("Users created succesfully!")

@user_router.post("/create_user")
async def create_user(params: Dict[str, str], session: AsyncSession = Depends(get_session),\
    token: str = Depends(oauth2_scheme)):

    if not await authenthicate_user(token, session):
        return create_response_bad("Token expired! Please login again!")
    
    try:
        user = User.AddNew(session, params)
    except Exception as e:
        return create_response_bad(str(e))
    
    return create_response_ok("User created!", user.to_dict())


@user_router.get("/get_user/{id}", )
async def create_users(id: int, session: AsyncSession = Depends(get_session),\
    token: str = Depends(oauth2_scheme)):

    if not await authenthicate_user(token, session):
        return create_response_bad("Token expired! Please login again!")
    user = await User.GetById(id, session)
    await session.close()

    return create_response_ok(user)


@user_router.post("/login")
async def login(params: Dict[str, str], session: AsyncSession = Depends(get_session)):

    if "email" not in params:
        return create_response_bad("Email is required")
    if "password" not in params:
        return create_response_bad("Password is required")

    users = await User.GetByArgs(session, {"email":params['email']})
    if len(users) > 1:
        return create_response_bad("More than 1 user has the same email")

    if not users:
        return create_response_bad("No user with such email found")

    user = users[0]

    if verify_password(params['password'], user.hashed_pass):
        token = create_access_token(params)
        return create_response_ok("User logged in!", {"token": token, "user":user.to_dict()})
    else:
        return create_response_bad("Incorrect password!")
        


@user_router.post("/sign-up")
async def sign_up(params: Dict[str, str], session: AsyncSession = Depends(get_session)):

    if "password" not in params:
        return create_response_bad("Password is not present")

    if "email" not in params:
        return create_response_bad("Email address is not present")

    if "username" not in params:
        return create_response_bad("Username is not present")

    password = params.pop("password")
    hashed_pass = await get_password_hash(password)
    params['hashed_pass'] = hashed_pass

    try:
        user = await User.AddNew(session, params)
    except Exception as e:
        return create_response_bad(str(e))
    finally:
        await session.close()

    return create_response_ok("User created!", user.to_dict())