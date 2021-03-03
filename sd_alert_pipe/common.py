from pydantic import BaseModel

from sd_alert_pipe.lasair import LasairService, LasairResult
from sd_alert_pipe.alerce import AlerceService, AlerceResult
from sd_alert_pipe.antares import AntaresService, AntaresResult


class RootResult(BaseModel):
    name: str
    lasair: LasairResult
    alerce: AlerceResult
    antares: AntaresResult


async def gather_data(name: str) -> RootResult:
    ls = LasairService()
    al = AlerceService()
    at = AntaresService()
    alerce_result = await al.get_result(name)
    lasair_result = await ls.get_result(name)
    antares_result = await at.get_result(name)
    rr = RootResult(
        name=name,
        lasair=lasair_result,
        alerce=alerce_result,
        antares=antares_result
    )
    return rr
