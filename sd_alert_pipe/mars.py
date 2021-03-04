from pydantic import BaseModel, HttpUrl
from typing import Optional
import logging
import httpx

from .exceptions import APIError, NoResultsError

logger = logging.getLogger(__name__)


class MarsResult(BaseModel):
    name: str
    broker_id: str
    url: HttpUrl
    ra: float
    dec: float
    data: Optional[dict]


class MarsService:
    broker = 'mars'

    def __init__(self):
        self.api_root = 'https://mars.lco.global'

    def broker_url(self, lco_id: int) -> str:
        return f'{self.api_root}/{lco_id}/'

    async def get_result(self, objectId: str) -> MarsResult:
        logger.info('getting MARS result.')
        async with httpx.AsyncClient() as client:
            r = await client.get(f'{self.api_root}/?objectId={objectId}&format=json')
            try:
                r.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise APIError(e)
            d = r.json()
            if len(d['results']) < 1:
                raise NoResultsError

            first_result = d['results'][0]
            logger.info('finished MARS query.')
            return MarsResult(
                name=first_result['objectId'],
                broker_id=first_result['lco_id'],
                url=self.broker_url(first_result['lco_id']),
                ra=first_result['candidate']['ra'],
                dec=first_result['candidate']['dec'],
                data=d
            )
