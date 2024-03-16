"""Photo controllers."""
import io

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse, Response

from fastapi import UploadFile
from controllers import (
    create_response,
    CurrentUser,
    ObjectStorageClient,
    CurrentAsyncSession,
    HttpSession,
)
from config import config
from data import PhotoResponseItem, Photo
from logger import log


photo_router = APIRouter(prefix="/photo", tags=["photo"])


@log()
@photo_router.post("/upload", response_model=PhotoResponseItem)
async def upload_photo(
    user: CurrentUser,
    object_client: ObjectStorageClient,
    session: CurrentAsyncSession,
    file: UploadFile | None = None,
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
    await object_client.put_object(
        photo_path, file, file.size, file.content_type
    )

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
        headers={
            "Content-Disposition": f'attachment; filename="{photo.photo_name}"'
        },
    )
