from enum import Enum
from dataclasses_json import Undefined, dataclass_json
from dataclasses import dataclass

API_HOST = "https://wallies.cacko.net/api"

class ENDPOINT(Enum):
    ARTWORKS = "artworks.json"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Artwork:
    title: str
    raw_src: str
    web_uri: str

