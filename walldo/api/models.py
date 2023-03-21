from enum import StrEnum
from pydantic import BaseModel, Extra


class ENDPOINT(StrEnum):
    ARTWORKS = "artworks.json"


class Artwork(BaseModel, extra=Extra.ignore):
    title: str
    raw_src: str
    web_uri: str
