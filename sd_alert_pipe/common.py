from pydantic import BaseModel, HttpUrl
from typing import Optional


class Alert(BaseModel):
    """Represents a result from a broker.

    Attributes

    data: The full set of unstructured data from the broker
    """
    name: str
    broker: str
    broker_id: str
    url: HttpUrl
    ra: float
    dec: float
    data: Optional[dict]
