"""Photo controllers."""
import io

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from fastapi import UploadFile
from controllers import (
    create_response,
    CurrentUser,
    ObjectStorageClient,
    CurrentAsyncSession,
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
    photo_path = photo.create_photos_path()
    await object_client.put_object(
        config.minio_bucket, photo_path, file, file.size, file.content_type
    )

    return create_response(
        message="Photo uploaded!",
        status=status.HTTP_200_OK,
        response_model=PhotoResponseItem,
        item={"photo_path": photo_path},
    )
