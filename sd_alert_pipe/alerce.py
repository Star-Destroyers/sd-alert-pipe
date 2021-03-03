from typing import Optional
import httpx
from pydantic import BaseModel, HttpUrl


class AlerceResult(BaseModel):
    name: str
    broker_id: str
    url: HttpUrl
    ra: float
    dec: float
    classification: dict
    data: Optional[dict]


class AlerceService:
    """Alerce broker interface.
    """
    def __init__(self):
        self.api_root = 'https://ztf.alerce.online'

    def get_url(self, objectId: str) -> str:
        return 'https://alerce.online/object/' + objectId

    async def get_result(self, objectId: str) -> AlerceResult:
        alert = await self.get_alert(objectId)
        classification = await self.get_probabilities(objectId)
        return AlerceResult(
            name=alert['oid'],
            broker_id=alert['oid'],
            url=self.get_url(alert['oid']),
            ra=alert['meanra'],
            dec=alert['meandec'],
            classification=classification,
            data=alert
        )

    async def get_alert(self, objectId: str) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.post(self.api_root + '/get_stats', json={'oid': objectId})
            r.raise_for_status()
            d = r.json()
            return d['result']['stats']

    async def get_probabilities(self, objectId: str) -> dict:
        """Returns a dictionary of type -> probability ML classifications
        for this object.
        """
        async with httpx.AsyncClient() as client:
            r = await client.post(self.api_root + '/get_probabilities', json={'oid': objectId})
            r.raise_for_status()
            d = r.json()
            return d['result']['probabilities']
