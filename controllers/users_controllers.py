"""Basic controllers for users."""

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from fastapi.templating import Jinja2Templates

from data import User, PydanticUser, PydanticUserSignUp

from controllers import create_response, CurrentUser, CurrentSession
from utils import (
    create_access_token,
    get_password_hash,
    verify_password,
)


user_router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory="templates")


@user_router.post("/create_user")
async def create_user(
    pydantic_user: PydanticUser,
    user: CurrentUser,
    session: CurrentSession,
):
    """Creating a simple user."""

    params = pydantic_user.dict()
    password = params.pop("password")
    hashed_pass = get_password_hash(password)
    params["hashed_pass"] = hashed_pass

    try:
        user = await User.AddNew(session, params)
    except Exception as e:
        return create_response(str(e), 400)

    return create_response("User created!", 200, user.serialize())


@user_router.get("/get_user/{id_user}")
async def get_user(
    id_user: int,
    user: CurrentUser,
    session: CurrentSession,
) -> ORJSONResponse:
    """Get user by id."""

    user = await User.GetById(session, id_user)

    if not user:
        return create_response("User not found!", 400)

    return create_response("User fetched!", 200, user.serialize())


@user_router.post("/login")
async def login(
    pydantic_user: PydanticUser,
    session: CurrentSession,
) -> ORJSONResponse:
    """Login controller for a user."""

    data = pydantic_user.dict(exclude_none=True)
    password = data.pop("password")
    users = await User.GetByArgs(session, data)

    if not users:
        return create_response(
            "No user with such email or username found", 400
        )

    user = users[0]

    if verify_password(password, user.hashed_pass):
        data = user.serialize()
        data.pop("id")
        data.pop("created_at")
        data.pop("updated_at")
        token = create_access_token(data)
        return create_response(
            "User logged in!", 200, {"token": token, "user": user.serialize()}
        )

    return create_response("Incorrect password!", 400)


@user_router.post("/sign-up")
async def sign_up(
    form: PydanticUserSignUp,
    session: CurrentSession,
) -> ORJSONResponse:
    """Sign-up controller for the user."""

    params = form.dict()
    password = params.pop("password")
    hashed_pass = get_password_hash(password)
    params["hashed_pass"] = hashed_pass

    try:
        user = await User.AddNew(session, params)
    except Exception as user_error:
        return create_response(str(user_error), 400)

    return create_response("User created!", 200, user.serialize())
