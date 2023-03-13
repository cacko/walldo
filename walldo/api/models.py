from enum import StrEnum
from pydantic import BaseModel


class ENDPOINT(StrEnum):
    ARTWORKS = "artworks.json"


class Artwork(BaseModel):
    title: str
    raw_src: str
    web_uri: str
    source: str
