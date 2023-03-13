from enum import StrEnum
from typing import Optional
from pydantic import BaseModel, Extra


class ENDPOINT(StrEnum):
    ARTWORKS = "artworks.json"


class Artwork(BaseModel, extra=Extra.ignore):
    title: str
    raw_src: str
    web_uri: str
    muzei_src: str
    source: str


class ArtworkResponse(BaseModel, extra=Extra.ignore):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: Optional[list[Artwork]]
