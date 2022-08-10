import logging
from tkinter import END
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from wallies.api.models import ENDPOINT, API_HOST, Artwork


class Client(object):

    def __call(self, path, **kwargs):
        try:
            url = f"{API_HOST}/{path}"
            resp = requests.get(url=url, **kwargs)
            return resp.json()
        except (ConnectTimeout, ConnectionError) as e:
            logging.error(e)
        return None

    def artworks(self) -> list[Artwork]:
        res = self.__call(ENDPOINT.ARTWORKS.value)
        if not res:
            return []
        return Artwork.schema().load(res, many=True)
