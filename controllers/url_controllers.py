"""Url controllers"""

from fastapi import APIRouter, status

from controllers import (
    create_response,
    CurrentUser,
    RedisAsyncClient,
)
from data import UrlPacket, UrlShortResponseItem
from utils import get_string_at_key, make_short_hash, store_string_at_key
from config import config

url_router = APIRouter(prefix="/url-short", tags=["url-short"])


@url_router.post("/set", response_model=UrlShortResponseItem)
async def create_url(
    url_packet: UrlPacket,
    _: CurrentUser,
    redis_client: RedisAsyncClient,
):
    """Make a short url controller"""

    str_hash = make_short_hash(str(url_packet.url))
    await store_string_at_key(redis_client, str(str_hash), str(url_packet.url))

    return create_response(
        message="Url made!",
        status=status.HTTP_200_OK,
        response_model=UrlShortResponseItem,
        item={"url": f"http://{config.domain_name}/url-short/get/{str_hash}"},
    )


@url_router.get("/get/{url_hash}", response_model=UrlShortResponseItem)
async def get_url(
    url_hash: str,
    _: CurrentUser,
    redis_client: RedisAsyncClient,
):
    """Get url at hash."""

    url_string = await get_string_at_key(redis_client, url_hash)

    return create_response(
        message="Url retrieved!",
        status=status.HTTP_307_TEMPORARY_REDIRECT,
        response_model=UrlShortResponseItem,
        item={"url": url_string},
    )
