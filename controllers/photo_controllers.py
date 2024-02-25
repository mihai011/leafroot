"""Photo controllers."""
import io

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from fastapi import UploadFile
from controllers import create_response, CurrentUser, ObjectStorageClient
from config import config
from data import PhotoResponseItem
from data import PhotoPacket
from logger import log


photo_router = APIRouter(prefix="/photo", tags=["photo"])


@log()
@photo_router.post("/upload", response_model=PhotoResponseItem)
async def upload_photo(
    _: CurrentUser,
    object_client: ObjectStorageClient,
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

    await object_client.put_object(
        config.minio_bucket, file.filename, file, file.size, file.content_type
    )

    return create_response(
        message="Photo uploaded!",
        status=status.HTTP_200_OK,
        response_model=PhotoResponseItem,
        item={"photo": file.filename},
    )
