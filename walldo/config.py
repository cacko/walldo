from pathlib import Path
from typing import Optional
from appdirs import user_cache_dir, user_config_dir, user_data_dir
import yaml
from walldo import __name__
from pydantic import BaseModel, Field
from walldo.core.models import Category, INTERVAL_OPTIONS


class UiConfig(BaseModel):
    category: Optional[Category] = Field(default=Category.MINIMAL.value)
    interval: Optional[int] = Field(default=60)

    @property
    def interval_text(self) -> str:
        try:
            res = next(filter(
                lambda x: x[0] == self.interval, INTERVAL_OPTIONS),
                None
            )
            assert res
            return res[1]
        except AssertionError:
            return "Nothing"


class APIConfig(BaseModel):
    host: Optional[str] = Field(
        default="https://wallies.cacko.net/api")


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

    @property
    def api_config(cls) -> APIConfig:
        return APIConfig(**cls().getvar("api"))

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
        self._config = yaml.full_load(self.__class__.app_config.read_text())
        print(list(self._config))

    def init(self):
        with open(app_config.app_config, "w") as fp:
            data = dict(
                ui=UiConfig().dict(),
                api=APIConfig().dict()
            )
            yaml.dump_all(documents=data, stream=fp)

    def getvar(self, var, *args, **kwargs):
        assert isinstance(self._config, dict)
        return self._config.get(var, *args, *kwargs)

    def __save(self):
        with open(app_config.app_config, "w") as fp:
            yaml.dump_all(documents=self._config, stream=fp)

    def setvar(self, var, value, *args, **kwargs):
        assert isinstance(self._config, dict)
        section, key = var.split(".")
        assert section
        assert key
        self._config[section][key] = value
        self.__save()
