from typing import Optional
import httpx
import logging
from pydantic import BaseModel, HttpUrl

from .exceptions import APIError

logger = logging.getLogger(__name__)


class EarlyProbabilities(BaseModel):
    agn: float
    sn: float
    vs: float
    asteroid: float
    bogus: float


class LateProbabilities(BaseModel):
    agn_i: float
    blazar: float
    cv_nova: float
    snia: float
    snibc: float
    snii: float
    sniin: float
    slsn: float
    ebsd_d: float
    ebc: float
    dsct: float
    rrl: float
    ceph: float
    lpv: float
    periodic_other: float


class Classification(BaseModel):
    type: str
    probability: float
    late: Optional[LateProbabilities]
    early: Optional[EarlyProbabilities]


class AlerceResult(BaseModel):
    name: str
    broker_id: str
    url: HttpUrl
    ra: float
    dec: float
    classification: Classification
    data: Optional[dict]


class AlerceService:
    """Alerce broker interface.
    """
    broker = 'alerce'

    def __init__(self):
        self.api_root = 'https://ztf.alerce.online'

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
            classification=classification,
            data=alert
        )

    async def get_alert(self, objectId: str) -> dict:
        async with httpx.AsyncClient() as client:
            r = await client.post(self.api_root + '/get_stats', json={'oid': objectId})
            r.raise_for_status()
            d = r.json()
            return d['result']['stats']

    async def get_probabilities(self, objectId: str) -> Classification:
        async with httpx.AsyncClient() as client:
            r = await client.post(self.api_root + '/get_probabilities', json={'oid': objectId})
            r.raise_for_status()
            d = r.json()
            early_raw = d['result']['probabilities']['early_classifier']
            late_raw = d['result']['probabilities']['late_classifier']
            early = {k.lower().replace('/', '_').replace('-', '_').replace('_prob', ''): v for k, v in early_raw.items() if v}
            late = {k.lower().replace('/', '_').replace('-', '_').replace('_prob', ''): v for k, v in late_raw.items() if v}
            early.pop('oid', '')
            late.pop('oid', '')
            early_max = max(early, key=early.get) if early else ''
            late_max = max(late, key=late.get) if late else ''
            if late_max:
                ctype = late_max
                probability = late[late_max]
            elif early_max:
                ctype = early_max
                probability = early[early_max]
            else:
                ctype = 'None'
                probability = 0
            early_prob = EarlyProbabilities(**early) if early else None
            late_prob = LateProbabilities(**late) if late else None

            return Classification(
                type=ctype, probability=probability, early=early_prob, late=late_prob
            )
