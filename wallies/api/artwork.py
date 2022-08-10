import requests
from wallies.core.string import string_hash
from pathlib import Path
from wallies.config import app_config


class ArtworkFile:

    __url = None

    def __init__(self, url) -> None:
        self.__url = url

    @property
    def __filename(self):
        return f"f{string_hash(self.__url)}.png"

    @property
    def path(self) -> Path:
        pth: Path = app_config.cache_dir / self.__filename
        if not pth.exists():
            resp = requests.get(self.__url)
            content = resp.content
            pth.write_bytes(content)
        return pth
