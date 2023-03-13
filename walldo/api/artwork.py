from corestring import string_hash
from pathlib import Path
from walldo.config import app_config
import requests


class ArtworkFile:

    def __init__(self, url: str) -> None:
        self.__url = url

    @property
    def filename(self):
        return f"f{string_hash(self.__url)}.png"

    @property
    def path(self) -> Path:
        pth: Path = app_config.cache_dir / self.filename
        if not pth.exists():
            resp = requests.get(self.__url)
            content = resp.content
            pth.write_bytes(content)
        return pth
