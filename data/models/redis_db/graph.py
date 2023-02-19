"""
Redis graph models."""

import uuid
from typing import Optional
from pydantic import BaseModel, Field, Json
from pydantic.typing import Any


class RedisGraph(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Graph Name",
            }
        }


class RedisNode(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    label: str = Field(...)
    properties: Json[Any]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "label": "Node label",
                "properties": {"key": "value"},
            }
        }
