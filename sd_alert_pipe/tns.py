from typing import List
import logging
import httpx
import json

from .config import settings
from .exceptions import APIError, NoResultsError

logger = logging.getLogger(__name__)


class TNSService:
    broker = 'tns'

    def __init__(self, sandbox=False):
        self.api_key = settings.TNS_API_KEY

        if sandbox:
            self.api_root = 'https://sandbox.wis-tns.org'
        else:
            self.api_root = 'https://www.wis-tns.org'

    async def cone_search(self, ra: float, dec: float) -> List[dict]:
        payload = {'api_key': self.api_key, 'data': json.dumps({'ra': ra, 'dec': dec})}

        async with httpx.AsyncClient() as client:
            r = await client.post(self.api_root + '/api/get/search', data=payload)
            try:
                r.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise APIError(e)

            d = r.json()

            if len(d['data']['reply']) < 1:
                raise NoResultsError

            return d['data']['reply']

    async def get_tns_object(self, objname: str) -> dict:
        payload = {'api_key': self.api_key, 'data': json.dumps({'objname': objname, 'photometry': 1})}

        async with httpx.AsyncClient() as client:
            r = await client.post(self.api_root + '/api/get/object', data=payload)

            try:
                r.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise APIError(e)

            d = r.json()
            if d['data']['reply'].get('name', {}).get('110'):
                # This has to be the worst "not found" response I've ever seen
                raise NoResultsError

            return d['data']['reply']
