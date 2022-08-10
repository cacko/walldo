from pathlib import Path
from appdir import get_app_dir
from wallies import __name__
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

DEFAULT_CONFIG = {
    "ui": {
        "interval": 60,
        "category": "minimal"
    },
    "storage": {
        "redis": "redis://127.0.0.1/4"
    }
}


class ConfigMeta(type):

    _instance = None

    def __call__(cls, *args, **kwds):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwds)
        return cls._instance

    @property
    def app_dir(cls) -> Path:
        ad = get_app_dir(__name__)
        if not ad.exists():
            ad.mkdir(parents=True)
        return ad

    @property
    def cache_dir(cls) -> Path:
        cache_dir = cls.app_dir / "cache"
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)
        return cache_dir

    @property
    def config_path(cls) -> Path:
        return cls.app_dir / "config.yaml"

    def get(cls, name, *args, **kwargs):
        return cls().getvar(name, *args, **kwargs)


class Config(object, metaclass=ConfigMeta):

    __dict: dict = {}

    def __init__(self, *args, **kwargs):
        if not __class__.config_path.exists():
            __class__.config_path.write_text(dump(DEFAULT_CONFIG, Dumper=Dumper))
        self.__dict = load(__class__.config_path.read_text(), Loader=Loader)

    def getvar(self, name, *args, **kwargs):
        return self.__dict.get(name, *args, **kwargs)
