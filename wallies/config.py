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
        "category": "minimal",
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

    def set(cls, name, value, *args, **kwargs):
        return cls().setvar(name, value, *args, **kwargs)


class app_config(object, metaclass=ConfigMeta):

    __dict: dict = {}

    def __init__(self, *args, **kwargs):
        if not __class__.config_path.exists():
            __class__.config_path.write_text(
                dump(DEFAULT_CONFIG, Dumper=Dumper))
            self.__dict = DEFAULT_CONFIG
        else:
            self.__dict = load(
                __class__.config_path.read_text(), Loader=Loader)

    def getvar(self, name, root=None, *args, **kwargs):
        if not root:
            root = self.__dict
        if '.' in name:
            rk, k = name.split('.', 1)
            return self.getvar(k, root=root.get(rk, {}), *args, **kwargs)
        else:
            return root.get(name, *args, **kwargs)

    def setvar(self, name, value, root=None, *args, **kwargs):
        if not root:
            root = self.__dict
        if '.' in name:
            rk, k = name.split('.', 1)
            return self.setvar(k, value, root=root.get(rk, {}), *args, **kwargs)
        else:
            return root.update(name, value, *args, **kwargs)
