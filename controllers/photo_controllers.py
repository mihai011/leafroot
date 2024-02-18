"""Photo controllers."""
from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from controllers import create_response, CurrentUser, ObjectStorageClient
from config import config
from data import PhotoResponseItem, PhotoResponse
from data import PhotoPacket
from logger import log


photo_router = APIRouter(prefix="/photo", tags=["photo"])


@log()
@photo_router.post("/upload", response_model=PhotoResponseItem)
async def upload_photo(
    photo_packet: PhotoPacket,
    _: CurrentUser,
    object_client: ObjectStorageClient,
) -> ORJSONResponse:
    """Upload a photo."""

    photo_name = ".".join([photo_packet.photo_name, photo_packet.photo_type])

    await object_client.put_object(photo_name, photo_packet.photo_body)

    return create_response(
        message="Photo uploaded!",
        status=status.HTTP_200_OK,
        response_model=PhotoResponseItem,
        item={"photo": photo_name},
    )
