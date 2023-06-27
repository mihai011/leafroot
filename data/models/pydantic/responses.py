"""Module for pydantic responses."""
from typing import Optional, Union, List, Dict, Any

from pydantic import BaseModel, UUID4


class BaseResponse(BaseModel):
    """Basic response."""

    message: str
    item: Optional[str]


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

    postgressql: Union[bool, str]
    redis: Union[bool, str]
    rabbitmq: Union[bool, str]
    mongo: Union[bool, str]
    spark: Union[bool, str]
    kafka: Union[bool, str]
    surrealdb: Union[bool, str]
    scylladb: Union[bool, str]


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
    """Response for task"""

    task_id: UUID4
    date_done: Optional[str]
    traceback: Optional[str]
    children: Optional[List[str]]
    result: Optional[Dict[Any, Any]]
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

    item: List[BookListResponse]


class ParticleResponse(BaseModel):
    """Response for particle."""

    charge: float
    atom_id: Optional[int]


class ParticleResponseItem(BaseResponse):
    """Response for particle item."""

    item: ParticleResponse


class ProtonResponse(BaseModel):
    """Response for proton list."""

    protons: List[ParticleResponse]


class ElectronResponse(BaseModel):
    """Response for electron list."""

    electrons: List[ParticleResponse]


class NeutronResponse(BaseModel):
    """Response for neutron list."""

    neutrons: List[ParticleResponse]


class ParticleResponseListItem(BaseResponse):
    """Response for particle list item."""

    item: Union[NeutronResponse, ProtonResponse, ElectronResponse]


class AtomResponse(BaseModel):
    """Response for atom."""

    x: float
    y: float
    z: float

    neutrons: Optional[List[ParticleResponse]]
    protons: Optional[List[ParticleResponse]]
    electrons: Optional[List[ParticleResponse]]


class AtomResponseItem(BaseResponse):
    """Respponse for atom item."""

    item: AtomResponse


class RedisGraphResponse(BaseModel):
    """Response for redis graph."""

    name: str
    nodes: List[str]
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

    result: List[List[Dict[Any, Any]]]


class RedisQueryResponseItem(BaseResponse):
    """Response for query result item."""

    item: RedisQueryResponse
