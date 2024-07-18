"""Key Value controllers."""

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from controllers import create_response, CurrentUser, MongoDatabase
from data import BaseResponse, KeyValuePacket

keyvalue_router = APIRouter(prefix="/keyvalue", tags=["keyvalue"])


@keyvalue_router.post("", response_model=BaseResponse)
async def add_key_value(
    _: CurrentUser, mongo_db: MongoDatabase, keyvalue: KeyValuePacket
) -> ORJSONResponse:
    """Add key value to database."""
    await mongo_db["keyvalue"].insert_one(
        {"key": keyvalue.key, "value": keyvalue.value}
    )
    return create_response(
        message="Key Value added!",
        status=status.HTTP_200_OK,
        response_model=BaseResponse,
        item=None,
    )


@keyvalue_router.get("/{key}", response_model=BaseResponse)
async def get_key_value(
    _: CurrentUser, mongo_db: MongoDatabase, key: str
) -> ORJSONResponse:
    """Get key value from database."""
    response = await mongo_db["keyvalue"].find_one({"key": key})
    if response:
        return create_response(
            message="Key Value retrieved!",
            status=status.HTTP_200_OK,
            response_model=BaseResponse,
            item=response["value"],
        )
    return create_response(
        message="Key Value not found!",
        status=status.HTTP_404_NOT_FOUND,
        response_model=BaseResponse,
        item=None,
    )


@keyvalue_router.delete("/{key}", response_model=BaseResponse)
async def delete_key_value(
    _: CurrentUser, mongo_db: MongoDatabase, key: str
) -> ORJSONResponse:
    """Delete key value from database."""
    response = await mongo_db["keyvalue"].delete_one({"key": key})
    if response.deleted_count:
        return create_response(
            message="Key Value deleted!",
            status=status.HTTP_200_OK,
            response_model=BaseResponse,
            item=None,
        )
    return create_response(
        message="Key Value not found!",
        status=status.HTTP_404_NOT_FOUND,
        response_model=BaseResponse,
        item=None,
    )
