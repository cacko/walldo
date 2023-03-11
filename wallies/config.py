from pathlib import Path
from typing import Optional
from appdirs import user_cache_dir, user_config_dir, user_data_dir
from yaml import Loader, load, dump
from wallies import __name__
from pydantic import BaseModel, Extra, Field
from wallies.ui.models import Categories


class UiConfig(BaseModel, extra=Extra.ignore):
    category: Optional[Categories] = Field(default=Categories.MINIMAL)
    interval: Optional[int] = Field(default=60)


class app_config_meta(type):
    _instance = None

    def __call__(self, *args, **kwds):
        if not self._instance:
            self._instance = super().__call__(*args, **kwds)
        return self._instance

    def get(cls, var, *args, **kwargs):
        return cls().getvar(var, *args, **kwargs)

    def set(cls, var, value, *args, **kwargs):
        return cls().setvar(var, value, *args, **kwargs)

    @property
    def config_dir(cls) -> Path:
        return Path(user_config_dir(__name__))

    @property
    def cache_dir(cls) -> Path:
        return Path(user_cache_dir(__name__))

    @property
    def data_dir(cls) -> Path:
        return Path(user_data_dir(__name__))

    @property
    def app_config(cls) -> Path:
        return cls.config_dir / "config.yaml"

    @property
    def ui_config(cls) -> UiConfig:
        return UiConfig(**cls().getvar("ui"))

    def is_configured(cls) -> bool:
        return True


class app_config(object, metaclass=app_config_meta):

    _config: Optional[dict] = None

    def __init__(self) -> None:
        if not app_config.cache_dir.exists():
            app_config.cache_dir.mkdir(parents=True, exist_ok=True)
        if not app_config.data_dir.exists():
            app_config.data_dir.mkdir(parents=True, exist_ok=True)
        if not app_config.app_config.exists():
            self.init()
        self._config = load(app_config.app_config.read_text(), Loader=Loader)

    def init(self):
        with open(app_config.app_config, "w") as fp:
            data = {
                "ui": UiConfig().dict(),
            }
            dump(data, fp)

    def getvar(self, var, *args, **kwargs):
        assert isinstance(self._config, dict)
        return self._config.get(var, *args, *kwargs)

    def __save(self):
        with open(app_config.app_config, "w") as fp:
            dump(self._config, fp)

    def setvar(self, var, value, *args, **kwargs):
        assert isinstance(self._config, dict)
        section, key = var.split(".")
        assert section
        assert key
        self._config[section][key] = value
        self.__save()
