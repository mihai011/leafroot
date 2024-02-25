"""Basic controllers for users."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import status

from data import (
    User,
    PydanticUser,
    PydanticUserSignUp,
    UserResponseItem,
    AuthorizedUserResponseItem,
    ErrorResponse,
)

from controllers import create_response, CurrentUser, CurrentAsyncSession
from utils import (
    create_access_token,
    get_password_hash,
    verify_password,
)


user_router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory="templates")


@user_router.post("/create_user", response_model=UserResponseItem)
async def create_user(
    pydantic_user: PydanticUser,
    user: CurrentUser,
    session: CurrentAsyncSession,
):
    """Creating a simple user."""

    params = pydantic_user.dict()
    password = params.pop("password")
    hashed_pass = get_password_hash(password)
    params["hashed_pass"] = hashed_pass

    user = await User.AddNew(session, params)

    return create_response(
        message="User created!",
        status=200,
        response_model=UserResponseItem,
        item=user.serialize(),
    )


@user_router.get("/get_user/{id_user}", response_model=UserResponseItem)
async def get_user(
    id_user: int,
    user: CurrentUser,
    session: CurrentAsyncSession,
) -> ORJSONResponse:
    """Get user by id."""

    user = await User.GetById(session, id_user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="No user found!"
        )

    return create_response(
        message="User fetched!",
        status=status.HTTP_200_OK,
        response_model=UserResponseItem,
        item=user.serialize(),
    )


@user_router.post(
    "/login",
    response_model=AuthorizedUserResponseItem,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
    },
)
async def login(
    pydantic_user: PydanticUser,
    session: CurrentAsyncSession,
) -> ORJSONResponse:
    """Login controller for a user."""

    data = pydantic_user.dict(exclude_none=True)
    password = data.pop("password")
    users = await User.GetByArgs(session, data)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user with such email or username found!",
        )

    user = users[0]
    item = {}

    if verify_password(password, user.hashed_pass):
        data = user.serialize()
        data.pop("id")
        data.pop("created_at")
        data.pop("updated_at")
        data.pop("photos")
        token = create_access_token(data)

        item["token"] = token
        item["user"] = user.serialize()
        return create_response(
            message="User logged in!",
            status=200,
            response_model=AuthorizedUserResponseItem,
            item=item,
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect Password!",
    )


@user_router.post(
    "/sign-up",
    response_model=UserResponseItem,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse}},
)
async def sign_up(
    form: PydanticUserSignUp,
    session: CurrentAsyncSession,
) -> ORJSONResponse:
    """Sign-up controller for the user."""

    params = form.dict()
    password = params.pop("password")
    hashed_pass = get_password_hash(password)
    params["hashed_pass"] = hashed_pass
    params["photos"] = []

    user = await User.AddNew(session, params)

    return create_response(
        message="User created!",
        status=status.HTTP_200_OK,
        response_model=UserResponseItem,
        item=user.serialize(),
    )
