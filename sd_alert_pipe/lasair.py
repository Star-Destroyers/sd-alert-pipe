from typing import List
import httpx
import logging
from httpx import Response
from pydantic import BaseModel, HttpUrl
from typing import Optional

from .config import settings
from .exceptions import APIError, NoResultsError

logger = logging.getLogger(__name__)

DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'


class Crossmatch(BaseModel):
    transient_object_id: str
    association_type: str
    catalogue_object_id: str
    catalogue_object_type: str
    catalogue_table_name: Optional[str] = ''
    raDeg: float
    decDeg: float
    separationArcsec: float
    northSeparationArcsec: float
    eastSeparationArcsec: float
    physical_separation_kpc: Optional[float]
    direct_distance: Optional[float]
    distance: Optional[float]
    z: Optional[float]
    photoZ: Optional[float]
    photoZErr: Optional[float]
    Mag: float
    MagFilter: str
    MagErr: Optional[float]
    classificationReliability: int


class Classification(BaseModel):
    type: str
    description: str
    crossmatches: List[Crossmatch]


class LasairResult(BaseModel):
    name: str
    broker_id: str
    url: HttpUrl
    ra: float
    dec: float
    rmag: float
    magrmax: float
    magrmin: float
    magrmean: float
    gmag: float
    maggmax: float
    maggmin: float
    maggmean: float
    classification: dict

    data: Optional[dict]


class LasairService:
    """Lasair broker service.
    """
    broker = 'lasair'

    def __init__(self, api_key=None):
        self.api_key = api_key or settings.LASAIR_API_KEY
        self.api_root = 'https://lasair-iris.roe.ac.uk'
        self.headers = {'Authorization': f'Token {self.api_key}'}

    def broker_url(self, objectId: str) -> str:
        return 'https://lasair-iris.roe.ac.uk/object/' + objectId

    async def _query(self, selected: str, tables: str, conditions: str) -> Response:
        async with httpx.AsyncClient() as client:
            data = {
                'selected': selected,
                'tables': 'objects',
                'conditions': conditions
            }
            return await client.post(self.api_root + '/api/query/', data=data, headers=self.headers)

    async def get_result(self, objectId: str) -> LasairResult:
        logger.info('getting lasair result.')
        d = await self.get_alert(objectId)
        classification = await self.get_probabilities(objectId)
        logger.info('lasair done')
        return LasairResult(
            broker_id=d['objectId'],
            url=self.broker_url(d['objectId']),
            name=d['objectId'],
            ra=d['ramean'],
            dec=d['decmean'],
            classification=classification,
            data=d,
            **d
        )

    async def get_alert(self, objectId: str) -> dict:
        """
        Fetches general information about an object
        """
        logger.info(f'Fetching Lasair info for {objectId}')
        selected = '*'
        conditions = f'objects.objectId="{objectId}"'
        tables = 'objects'
        r = await self._query(selected, tables, conditions)
        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(e)

        if len(r.json()) < 1:
            raise NoResultsError

        return r.json()[0]

    async def fetch_watchlist(self, watchlist: int) -> List[LasairResult]:
        logger.info(f'Fetching Lasair results for watchlist {watchlist}')
        selected = """objects.objectId,
        objects.ramean,
        objects.decmean,
        objects.gmag,
        objects.rmag
        """
        conditions = '1=1'
        tables = f'objects, watchlist:{watchlist}'

        r = await self._query(selected, tables, conditions)
        r.raise_for_status()
        return [
            LasairResult(
                broker_id=result['objectId'],
                url=self.broker_url(result['objectId']),
                name=result['objectId'],
                ra=result['ramean'],
                dec=result['decmean'],
                data=result
            ) for result in r.json()
        ]

    async def get_probabilities(self, objectId: str) -> Classification:
        async with httpx.AsyncClient() as client:
            data = {'objectIds': objectId, 'lite': True}
            r = await client.post(self.api_root + '/api/sherlock/objects/', json=data, headers=self.headers)
            try:
                r.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise APIError(e)

            result = r.json()

            return Classification(
                type=result['classifications'][objectId][0],
                description=result['classifications'][objectId][1],
                crossmatches=[Crossmatch(**r) for r in result['crossmatches']]
            )

    async def stored_query(self, query_name: str) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.get(f'{self.api_root}/lasair/static/streams/{query_name}')
            try:
                r.raise_for_status()
                return r.json()
            except Exception as e:
                return {'error': str(e)}
