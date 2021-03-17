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
        timeout = httpx.Timeout(10, read=30)  # Mars can be pretty slow
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.get(f'{self.api_root}/?objectId={objectId}&format=json')
            try:
                r.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise APIError(e)
            d = r.json()
            if len(d['results']) < 1:
                raise NoResultsError

            broker_id = d['results'][0]['lco_id']

            r2 = await client.get(f'{self.api_root}/{broker_id}/?format=json')
            try:
                r2.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise APIError(e)

            details = r2.json()

            logger.info('finished MARS query.')
            return MarsResult(
                name=details['objectId'],
                broker_id=broker_id,
                url=self.broker_url(broker_id),
                ra=details['candidate']['ra'],
                dec=details['candidate']['dec'],
                data=details
            )
