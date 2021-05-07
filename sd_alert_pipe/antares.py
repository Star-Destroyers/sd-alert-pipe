from typing import Optional, List
import httpx
import json
import logging
from pydantic import BaseModel, HttpUrl

from .exceptions import APIError, NoResultsError

logger = logging.getLogger(__name__)


class AntaresResult(BaseModel):
    name: str
    broker_id: str
    url: HttpUrl
    ra: float
    dec: float
    crossmatch: List[str]
    data: Optional[dict]


class AntaresService:
    """Antares broker interface.

    Code is inspired by the antares client:
    https://gitlab.com/nsf-noirlab/csdc/antares/client

    But avoiding dependencies such as kafka and numpy, etc
    was desired.
    """
    broker = 'antares'

    def __init__(self, *args, **kwargs) -> None:
        self.api_root = 'https://api.antares.noirlab.edu/v1/'

    def broker_url(self, antaresId: str) -> str:
        return f'https://antares.noirlab.edu/loci/{antaresId}'

    async def get_result(self, objectId: str) -> AntaresResult:
        logger.info('getting ANTARES result')
        query = {
                    "query": {
                        "bool": {
                            "filter": {
                                "term": {"properties.ztf_object_id": objectId},
                            },
                        },
                    },
                }

        params = {
            "sort": "-properties.newest_alert_observation_time",
            "elasticsearch_query[locus_listing]": json.dumps(query),
        }
        async with httpx.AsyncClient() as client:
            r = await client.get(self.api_root + 'loci', params=params)
            try:
                r.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise APIError(e)
            d = r.json()

            if len(d['data']) < 1:
                raise NoResultsError

            logger.info('finished getting Antares result')

            return AntaresResult(
                name=d['data'][0]['attributes']['properties']['ztf_object_id'],
                broker_id=d['data'][0]['id'],
                url=self.broker_url(d['data'][0]['id']),
                ra=d['data'][0]['attributes']['ra'],
                dec=d['data'][0]['attributes']['dec'],
                crossmatch=d['data'][0]['attributes']['catalogs'],
                data=d
            )
