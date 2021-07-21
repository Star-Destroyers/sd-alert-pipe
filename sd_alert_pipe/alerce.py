from typing import Optional, List
import httpx
import logging
from pydantic import BaseModel, HttpUrl
from operator import attrgetter

from .exceptions import APIError

logger = logging.getLogger(__name__)


class Classification(BaseModel):
    classifier_name: str
    classifier_version: str
    class_name: str
    probability: float
    ranking: int


class AlerceResult(BaseModel):
    name: str
    broker_id: str
    url: HttpUrl
    ra: float
    dec: float
    classifications: List[Classification]
    data: Optional[dict]


class AlerceService:
    """Alerce broker interface.
    """
    broker = 'alerce'

    def __init__(self):
        self.api_root = 'http://api.alerce.online/ztf/v1/'

    def get_url(self, objectId: str) -> str:
        return 'https://alerce.online/object/' + objectId

    async def get_result(self, objectId: str) -> AlerceResult:
        logger.info('Getting alerce result.')
        try:
            alert = await self.get_alert(objectId)
            classification = await self.get_probabilities(objectId)
        except httpx.HTTPStatusError as e:
            raise APIError(e)

        logger.info('Finished getting alerce result.')
        return AlerceResult(
            name=alert['oid'],
            broker_id=alert['oid'],
            url=self.get_url(alert['oid']),
            ra=alert['meanra'],
            dec=alert['meandec'],
            classifications=classification,
            data=alert
        )

    async def get_alert(self, objectId: str) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.get(f'{self.api_root}objects/{objectId}')
            r.raise_for_status()
            d = r.json()
            return d

    async def get_probabilities(self, objectId: str) -> List[Classification]:
        async with httpx.AsyncClient() as client:
            r = await client.get(f'{self.api_root}objects/{objectId}/probabilities')
            r.raise_for_status()
            d = r.json()
            classifications: List[Classification] = [Classification(**classification) for classification in d]
            classifications.sort(key=attrgetter('probability'), reverse=True)
            classifications.sort(key=attrgetter('ranking'))

            return classifications
