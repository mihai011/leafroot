"""Redis graph models."""

import uuid
from typing import Optional
from pydantic import BaseModel, Field
from typing import Any, Dict


class RedisGraph(BaseModel):
    """Graph class for Redis."""

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)

    class Config:
        """Class Config for Redis Graph."""

        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Graph Name",
            }
        }


class RedisNode(BaseModel):
    """Node class for redis graph."""

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    graph: str
    label: str
    properties: Dict[str, Any]

    class Config:
        """Class Config for Redis Node."""

        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "label": "Node label",
                "properties": {"key": "value"},
            }
        }


class RedisEdge(BaseModel):
    """Redis edge class for graph."""

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    graph: str
    source: str
    destination: str
    relation: str
    properties: Optional[Dict[str, Any]]

    class Config:
        """Class Config for Redis Edge."""

        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "graph": "Graph Name",
                "source": "Source node",
                "destination": "Destination source",
                "relation": "Relation ",
            }
        }


class RedisGraphQuery(BaseModel):
    """Redis Pydantic Graph Class."""

    graph: str
    query: str

    class Config:
        """Class Config for Redis Query."""

        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "graph": "Graph Name",
                "query": "MATCH (p:president)-[:born]->(:state {name:'Hawaii'}) RETURN p",
            }
        }
