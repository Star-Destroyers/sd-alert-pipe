from typing import List
import httpx
import logging
from httpx import Response

from .config import settings
from .common import Alert

logger = logging.getLogger(__name__)


class LasairService:
    """Lasair broker service.
    """
    def __init__(self):
        self.api_key = settings.LASAIR_API_KEY
        self.api_root = 'https://lasair-iris.roe.ac.uk'
        self.headers = {'Authorization': f'Token {self.api_key}'}

    def broker_url(self, objectId: str) -> str:
        return 'https://lasair-iris.roe.ac.uk/object/' + objectId

    def _query(self, selected: str, tables: str, conditions: str) -> Response:

        data = {
            'selected': selected,
            'tables': 'objects',
            'conditions': conditions
        }
        return httpx.post(self.api_root + '/api/query/', data=data, headers=self.headers)

    def get_alert(self, objectId: str) -> Alert:
        selected = '*'
        conditions = f'objects.objectId="{objectId}"'
        tables = 'objects'
        r = self._query(selected, tables, conditions)
        r.raise_for_status()
        d = r.json()[0]
        return Alert(
            broker='LASAIR',
            broker_id=d['objectId'],
            url=self.broker_url(d['objectId']),
            name=d['objectId'],
            ra=d['ramean'],
            dec=d['decmean'],
            data=d
        )

    def fetch_watchlist(self, watchlist: int) -> List[Alert]:
        logger.info(f'Fetching Lasair results for watchlist {watchlist}')
        selected = """objects.objectId,
        objects.ramean,
        objects.decmean,
        objects.gmag
        """
        conditions = '1=1'
        tables = f'objects, watchlist:{watchlist}'

        r = self._query(selected, tables, conditions)
        r.raise_for_status()
        d = r.json()
        return [
            Alert(
                broker='LASAIR',
                broker_id=d['objectId'],
                url=self.broker_url(d['objectId']),
                name=d['objectId'],
                ra=d['ramean'],
                dec=d['decmean'],
                data=result
            ) for result in r.json()
        ]

    def get_probabilities(self, objectId: str) -> dict:
        data = {'objectIds': objectId, 'lite': True}
        r = httpx.post(self.api_root + '/api/sherlock/objects/', json=data, headers=self.headers)
        return r.json()
