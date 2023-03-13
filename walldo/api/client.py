import logging
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from walldo.api.models import ENDPOINT, Artwork
from walldo.config import app_config
from walldo.core.models import Category, Source
from typing import Optional


class Client(object):

    def __call(self, path, **kwargs):
        try:
            url = f"{app_config.api_config.host}/{path}"
            resp = requests.get(url=url, **kwargs)
            return resp.json()
        except (ConnectTimeout, ConnectionError) as e:
            logging.error(e)
        return None

    def artworks(
        self,
        category: Category,
        source: Source
    ) -> Optional[list[Artwork]]:
        in_category = category.value if category != Category.WHATEVER else None
        res = self.__call(ENDPOINT.ARTWORKS.value, params=dict(
            Category__in=in_category,
            Source__in=source.value
        ))
        if not res:
            return None
        return [Artwork(**x) for x in res]
