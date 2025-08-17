"""Module for pydantic responses."""

from __future__ import annotations

from typing import Any

from pydantic import UUID4, BaseModel, HttpUrl


class BaseResponse(BaseModel):
    """Basic response."""

    message: str
    item: str | bool | int | float | dict | list | None


class BaseMeta(BaseModel):
    """Meta data for responses."""

    id: int
    created_at: str
    updated_at: str


class UserResponse(BaseMeta):
    """Response for user."""

    username: str
    email: str


class UserResponseItem(BaseResponse):
    """Response for user item."""

    item: UserResponse


class AuthorizedUserResponse(BaseModel):
    """Response for authorized user."""

    token: str
    user: UserResponse


class AuthorizedUserResponseItem(BaseModel):
    """Response for authorized user item."""

    item: AuthorizedUserResponse


class ErrorResponse(BaseModel):
    """Response for error."""

    detail: str


class StatusResponse(BaseModel):
    """Response for status."""

    postgressql: bool | None
    redis: bool | None
    rabbitmq: bool | None
    mongo: bool | None
    spark: bool | None
    kafka: bool | None
    surrealdb: bool | None
    scylladb: bool | None
    cassandradb: bool | None


class StatusResponseItem(BaseResponse):
    """Response for status item."""

    item: StatusResponse


class QuoteResponse(BaseModel):
    """Response for quote."""

    quote: str
    author: str


class QuoteResponseItem(BaseResponse):
    """Response for quote item."""

    item: QuoteResponse


class TaskResponse(BaseModel):
    """Response for task."""

    task_id: UUID4
    date_done: str | None = None
    traceback: str | None = None
    children: list[str] | None = None
    result: dict[Any, Any] | None
    status: str


class TaskResponseItem(BaseResponse):
    """Response for task item."""

    item: TaskResponse


class BookListResponse(BaseModel):
    """Response for book."""

    id: UUID4
    title: str
    author: str
    synopsis: str


class BookListResponseItem(BaseResponse):
    """Response for book item."""

    item: list[BookListResponse]


class ParticleResponse(BaseModel):
    """Response for particle."""

    charge: float
    atom_id: int | None


class ParticleResponseItem(BaseResponse):
    """Response for particle item."""

    item: ParticleResponse


class ProtonResponse(BaseModel):
    """Response for proton list."""

    protons: list[ParticleResponse]


class ElectronResponse(BaseModel):
    """Response for electron list."""

    electrons: list[ParticleResponse]


class NeutronResponse(BaseModel):
    """Response for neutron list."""

    neutrons: list[ParticleResponse]


class ParticleResponseListItem(BaseResponse):
    """Response for particle list item."""

    item: NeutronResponse | ProtonResponse | ElectronResponse


class AtomResponse(BaseModel):
    """Response for atom."""

    x: float
    y: float
    z: float
    id: int

    neutrons: list[ParticleResponse] | None
    protons: list[ParticleResponse] | None
    electrons: list[ParticleResponse] | None


class AtomResponseItem(BaseResponse):
    """Respponse for atom item."""

    item: AtomResponse


class RedisGraphResponse(BaseModel):
    """Response for redis graph."""

    name: str
    nodes: list[str]
    edges: int


class RedisGraphResponseItem(BaseResponse):
    """Response for redis graph item."""

    item: RedisGraphResponse


class RedisNodeResponse(BaseModel):
    """Response for redis node."""

    alias: str


class RedisNodeResponseItem(BaseResponse):
    """Response for redis node item."""

    item: RedisNodeResponse


class RedisQueryResponse(BaseModel):
    """Response for query result."""

    result: list[list[dict[Any, Any]]]


class RedisQueryResponseItem(BaseResponse):
    """Response for query result item."""

    item: RedisQueryResponse


class MessageResponse(BaseModel):
    """Response Message Model."""

    user_id: UUID4
    message_id: UUID4
    text: str


class MessageResponseItem(BaseResponse):
    """Message Response Item."""

    item: MessageResponse


class MessageBoardResponse(BaseModel):
    """Response MessageBoard Model."""

    board: UUID4
    name: str
    messages: list[MessageResponse] | None


class MessageBoardResponseItem(BaseResponse):
    """Message Board Response Item."""

    item: MessageBoardResponse


class UrlShortReponse(BaseModel):
    """Base Response for Url Short."""

    url: HttpUrl


class UrlShortResponseItem(BaseResponse):
    """Url Short response Item."""

    item: UrlShortReponse


class PhotoResponse(BaseModel):
    """Response for photo."""

    photo_id: str


class PhotoResponseItem(BaseResponse):
    """Response for photo item."""

    item: PhotoResponse


class PhotoResponseListItem(BaseResponse):
    """Response for photo list item."""

    item: list[PhotoResponse]


class PhotoInfoResponse(BaseModel):
    """Response for photo info."""

    photo_id: int
    photo_name: str
    photo_size: int
    photo_type: str
    photo_hash: str


class PhotoInfoResponseItem(BaseModel):
    """Response for photo info item."""

    item: PhotoInfoResponse


class PhotoInfoResponseListItem(BaseModel):
    """Response for photo list."""

    item: list[PhotoInfoResponse]
