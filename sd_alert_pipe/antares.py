import httpx
import json

from .common import Alert


class AntaresService:
    """Antares broker interface.

    Code is inspired by the antares client:
    https://gitlab.com/nsf-noirlab/csdc/antares/client

    But avoiding dependencies such as kafka and numpy, etc
    was desired.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.api_root = 'https://api.antares.noirlab.edu/v1/'

    def get_alert(self, objectId: str) -> Alert:
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

        r = httpx.get(self.api_root + '/loci', params=params)
        r.raise_for_status()
        d = r.json()
        alert = Alert(
            name=d['data'][0]['attributes']['properties']['ztf_object_id'],
            broker='ANTARES',
            broker_id=d['data'][0]['id'],
            url=d['links']['self'],
            ra=d['data'][0]['attributes']['ra'],
            dec=d['data'][0]['attributes']['dec'],
            data=d
        )

        return alert
