from typing import Optional
import httpx
import json
from pydantic import BaseModel, HttpUrl


class AntaresResult(BaseModel):
    name: str
    broker_id: str
    url: HttpUrl
    ra: float
    dec: float
    data: Optional[dict]


class AntaresService:
    """Antares broker interface.

    Code is inspired by the antares client:
    https://gitlab.com/nsf-noirlab/csdc/antares/client

    But avoiding dependencies such as kafka and numpy, etc
    was desired.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.api_root = 'https://api.antares.noirlab.edu/v1/'

    async def get_result(self, objectId: str) -> AntaresResult:
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
            r = await client.get(self.api_root + '/loci', params=params)
            r.raise_for_status()
            d = r.json()
            alert = AntaresResult(
                name=d['data'][0]['attributes']['properties']['ztf_object_id'],
                broker_id=d['data'][0]['id'],
                url=d['links']['self'],
                ra=d['data'][0]['attributes']['ra'],
                dec=d['data'][0]['attributes']['dec'],
                data=d
            )

            return alert
