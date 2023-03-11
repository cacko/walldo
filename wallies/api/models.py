from enum import StrEnum
from pydantic import BaseModel

API_HOST = "https://wallies.cacko.net/api"


class ENDPOINT(StrEnum):
    ARTWORKS = "artworks.json"


class Artwork(BaseModel):
    title: str
    raw_src: str
    web_uri: str
    source: str
