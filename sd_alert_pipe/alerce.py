from .common import Alert
import httpx


class AlerceService:
    """Alerce broker interface.
    """
    def __init__(self):
        self.api_root = 'https://ztf.alerce.online'

    def get_url(self, objectId: str) -> str:
        return 'https://alerce.online/object/' + objectId

    def get_alert(self, objectId: str) -> Alert:
        r = httpx.post(self.api_root + '/get_stats', json={'oid': objectId})
        r.raise_for_status()
        d = r.json()
        stats = d['result']['stats']
        return Alert(
            name=stats['oid'],
            broker='ALERCE',
            broker_id=stats['oid'],
            url=self.get_url(stats['oid']),
            ra=stats['meanra'],
            dec=stats['meandec'],
            data=stats
        )

    def get_probabilities(self, objectId: str) -> dict:
        """Returns a dictionary of type -> probability ML classifications
        for this object.
        """
        r = httpx.post(self.api_root + '/get_probabilities', json={'oid': objectId})
        r.raise_for_status()
        d = r.json()
        return d['result']['probabilities']
