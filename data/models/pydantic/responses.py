"""
Added data from particles
"""
from typing import Optional, Union, List, Dict, Any

from pydantic import BaseModel, UUID4


class BaseResponse(BaseModel):
    message: str
    item: Optional[str]


class BaseMeta(BaseModel):
    id: int
    created_at: str
    updated_at: str


class UserResponse(BaseMeta):
    username: str
    email: str


class UserResponseItem(BaseResponse):
    item: UserResponse


class AuthorizedUserResponse(BaseModel):
    token: str
    user: UserResponse


class AuthorizedUserResponseItem(BaseModel):
    item: AuthorizedUserResponse


class ErrorResponse(BaseModel):
    detail: str


class StatusResponse(BaseModel):
    postgressql: Union[bool, str]
    redis: Union[bool, str]
    rabbitmq: Union[bool, str]
    mongo: Union[bool, str]


class StatusResponseItem(BaseResponse):
    item: StatusResponse


class QuoteResponse(BaseModel):
    quote: str
    author: str


class QuoteResponseItem(BaseResponse):
    item: QuoteResponse


class TaskResponse(BaseModel):
    task_id: UUID4
    date_done: Optional[str]
    traceback: Optional[str]
    children: Optional[List[str]]
    result: Optional[Dict[Any, Any]]
    status: str


class TaskResponseItem(BaseResponse):
    item: TaskResponse


class BookListResponse(BaseModel):
    id: UUID4
    title: str
    author: str
    synopsis: str


class BookListResponseItem(BaseResponse):
    item: List[BookListResponse]


class ParticleResponse(BaseModel):
    charge: float
    atom_id: Optional[int]


class ParticleResponseItem(BaseResponse):
    item: ParticleResponse


class ProtonResponse(BaseModel):
    protons: List[ParticleResponse]


class ElectronResponse(BaseModel):
    electrons: List[ParticleResponse]


class NeutronResponse(BaseModel):
    neutrons: List[ParticleResponse]


class ParticleResponseListItem(BaseResponse):
    item: Union[NeutronResponse, ProtonResponse, ElectronResponse]


class AtomResponse(BaseModel):
    x: float
    y: float
    z: float

    neutrons: Optional[List[ParticleResponse]]
    protons: Optional[List[ParticleResponse]]
    electrons: Optional[List[ParticleResponse]]


class AtomResponseItem(BaseResponse):
    item: AtomResponse


class RedisGraphResponse(BaseModel):
    name: str
    nodes: List[str]
    edges: int


class RedisGraphResponseItem(BaseResponse):
    item: RedisGraphResponse


class RedisNodeResponse(BaseModel):
    alias: str


class RedisNodeResponseItem(BaseResponse):
    item: RedisNodeResponse


class RedisEdgeResponse(BaseModel):
    pass


class RedisQueryResponse(BaseModel):
    result: List[List[Dict[Any, Any]]]


class RedisQueryResponseItem(BaseResponse):
    item: RedisQueryResponse
