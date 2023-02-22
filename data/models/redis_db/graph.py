"""
Redis graph models."""

import uuid
from typing import Optional
from pydantic import BaseModel, Field, UUID4
from pydantic.typing import Any, Dict


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
    graph: str
    label: str
    properties: Dict[str, Any]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "label": "Node label",
                "properties": {"key": "value"},
            }
        }


class RedisEdge(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    graph: str
    source: str
    destination: str
    relation: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "graph": "Graph Name",
                "source": "Source node",
                "destination": "Destination source",
                "relation": "Relation ",
            }
        }
