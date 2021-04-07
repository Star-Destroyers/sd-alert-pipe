from pydantic import BaseModel
from typing import Optional, List
import asyncio

from sd_alert_pipe.exceptions import APIError, NoResultsError
from sd_alert_pipe.lasair import LasairService, LasairResult
from sd_alert_pipe.alerce import AlerceService, AlerceResult
from sd_alert_pipe.antares import AntaresService, AntaresResult
from sd_alert_pipe.mars import MarsService, MarsResult

ENABLED_SERVICES = [LasairService(), AlerceService(), AntaresService(), MarsService()]


class FailedResult(BaseModel):
    broker: str
    error: str


class CommonResult(BaseModel):
    ra: float
    dec: float


class RootResult(BaseModel):
    name: str
    common: Optional[CommonResult]
    lasair: Optional[LasairResult]
    alerce: Optional[AlerceResult]
    antares: Optional[AntaresResult]
    mars: Optional[MarsResult]
    failed: List[FailedResult] = []

    @property
    def has_failed(self):
        return len(self.failed) > 0

    def set_general(self):
        if self.mars:
            self.common = CommonResult(ra=self.mars.ra, dec=self.mars.dec)
        elif self.lasair:
            self.common = CommonResult(ra=self.lasair.ra, dec=self.lasair.dec)
        elif self.alerce:
            self.common = CommonResult(ra=self.alerce.ra, dec=self.alerce.dec)
        elif self.antares:
            self.common = CommonResult(ra=self.antares.ra, dec=self.antares.dec)
        else:
            self.common = None


async def gather_data(name: str) -> RootResult:
    rr = RootResult(name=name)
    gathered = await asyncio.gather(*[service.get_result(name) for service in ENABLED_SERVICES], return_exceptions=True)
    for idx, result in enumerate(gathered):
        error = ''
        if isinstance(result, APIError):
            error = 'API Error. The response was: ' + str(result)
        elif isinstance(result, NoResultsError):
            error = 'No results for query'
        elif isinstance(result, Exception):
            error = 'Unexpected excpetion: ' + str(result)
        if error:
            fr = FailedResult(broker=ENABLED_SERVICES[idx].broker, error=error)
            rr.failed.append(fr)
        else:
            setattr(rr, ENABLED_SERVICES[idx].broker, result)
    rr.set_general()
    return rr
