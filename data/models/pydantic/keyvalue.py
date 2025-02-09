"""KeyValues packet model"""

from typing import Union
from pydantic import BaseModel


class KeyValuePacket(BaseModel):
    """KeyValue Packet"""

    key: str
    value: Union[int, str]
