"""Photo controllers."""

import io
from typing import Optional

from fastapi import APIRouter, UploadFile, status
from fastapi.responses import ORJSONResponse, Response

from controllers import (
    CurrentAsyncSession,
    CurrentUser,
    HttpSession,
    ObjectStorageClient,
    create_response,
)
from data import (
    BaseResponse,
    Photo,
    PhotoResponseItem,
    PhotoResponseListItem,
    UserFollowRelation,
)
from logger import log

photo_router = APIRouter(prefix="/photo", tags=["photo"])


@log()
@photo_router.post("/upload", response_model=PhotoResponseItem)
async def upload_photo(
    user: CurrentUser,
    object_client: ObjectStorageClient,
    session: CurrentAsyncSession,
    file: Optional[UploadFile] | None = None,
) -> ORJSONResponse:
    """Upload a photo."""

    if not file:
        return create_response(
            message="No photo uploaded!",
            status=status.HTTP_400_BAD_REQUEST,
            response_model=PhotoResponseItem,
            item={"photo": None},
        )

    photo_packet = {
        "user_id": user.id,
        "photo_name": file.filename,
    }

    photo = await Photo.AddNew(session, photo_packet)
    photo_path = photo.create_storage_path()
    file_bytes = io.BytesIO(await file.read())
    await object_client.put_object(photo_path, file_bytes, file.size, file.content_type)

    return create_response(
        message="Photo uploaded!",
        status=status.HTTP_200_OK,
        response_model=PhotoResponseItem,
        item={"photo_id": str(photo.uuid)},
    )


@log()
@photo_router.get("/download/{photo_id}")
async def download_photo(
    photo_id: str,
    object_client: ObjectStorageClient,
    session: CurrentAsyncSession,
    http_session: HttpSession,
) -> Response:
    """Download a photo."""

    photo_res = await Photo.GetByArgs(session, {"uuid": photo_id})

    if len(photo_res) == 0:
        return create_response(
            message="No photo found!",
            status=status.HTTP_400_BAD_REQUEST,
            response_model=PhotoResponseItem,
            item={"photo": None},
        )
    photo = photo_res[0]

    photo_path = photo.create_storage_path()
    response = await object_client.get_object(photo_path, http_session)

    return Response(
        content=await response.content.read(),
        media_type=response.content_type,
        headers={"Content-Disposition": f'attachment; filename="{photo.photo_name}"'},
    )


@log()
@photo_router.get("/list/{user_id}", response_model=PhotoResponseListItem)
async def list_photos(
    user_id: int, session: CurrentAsyncSession, user: CurrentUser
) -> Response:
    """List all photos."""

    if user_id != user.id:
        relation = await UserFollowRelation.GetByArgs(
            session, {"follower_id": user.id, "followed_id": user_id}
        )
        if not relation:
            return create_response(
                message="User is not following!",
                status=status.HTTP_400_BAD_REQUEST,
                response_model=PhotoResponseListItem,
                item=[],
            )
    photos = await Photo.GetByArgs(session, {"user_id": user_id})
    return create_response(
        message="Photos listed!",
        status=status.HTTP_200_OK,
        response_model=PhotoResponseListItem,
        item=[{"photo_id": str(photo.uuid)} for photo in photos],
    )


@log()
@photo_router.post("/follow/{user_id}", response_model=BaseResponse)
async def follow_user(
    user_id: int, session: CurrentAsyncSession, user: CurrentUser
) -> Response:
    """Follow a user."""

    relation = await UserFollowRelation.GetByArgs(
        session, {"follower_id": user.id, "followed_id": user_id}
    )
    if relation:
        return create_response(
            message="User is already following!",
            status=status.HTTP_400_BAD_REQUEST,
            response_model=BaseResponse,
            item=None,
        )
    await UserFollowRelation.AddNew(
        session, {"follower_id": user.id, "followed_id": user_id}
    )
    return create_response(
        message="User followed!",
        status=status.HTTP_200_OK,
        response_model=BaseResponse,
        item=None,
    )


@log()
@photo_router.delete("/delete/{photo_id}", response_model=PhotoResponseItem)
async def delete_photo(
    photo_id: str,
    object_client: ObjectStorageClient,
    session: CurrentAsyncSession,
    _: CurrentUser,
) -> Response:
    """Download a photo."""

    photo_res = await Photo.GetByArgs(session, {"uuid": photo_id})

    if len(photo_res) == 0:
        return create_response(
            message="No photo found!",
            status=status.HTTP_400_BAD_REQUEST,
            response_model=PhotoResponseItem,
            item={"photo": None},
        )
    photo = photo_res[0]

    photo_path = photo.create_storage_path()
    await object_client.remove_object(photo_path)

    return create_response(
        message="Photo deleted!",
        status=status.HTTP_200_OK,
        response_model=PhotoResponseItem,
        item={"photo_id": photo_id},
    )
