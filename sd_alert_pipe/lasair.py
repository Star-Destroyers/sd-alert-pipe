from typing import List
import httpx
import logging

from .config import settings
from .common import Alert

logger = logging.getLogger(__name__)


class LasairService:
    """Lasair broker service.
    """
    def __init__(self):
        self.api_key = settings.LASAIR_API_KEY
        self.api_root = 'https://lasair-iris.roe.ac.uk/api/query/'

    def broker_url(self, objectId: str) -> str:
        return 'https://lasair-iris.roe.ac.uk/object/' + objectId

    def fetch_watchlist(self, watchlist: int) -> List[Alert]:
        selected = """objects.objectId,
        objects.ramean,
        objects.decmean,
        objects.gmag
        """

        conditions = """1=1
        """

        headers = {'Authorization': f'Token {self.api_key}'}

        logger.info(f'Fetching Lasair results for watchlist {watchlist}')
        data = {
            'selected': selected,
            'tables': f'objects, watchlist:{watchlist}',
            'conditions': conditions
        }

        r = httpx.post(self.api_root, data=data, headers=headers)
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
