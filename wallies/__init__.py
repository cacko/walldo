import logging
from os import environ
from cachable.cacheable import Cachable
from wallies.ui.app import WalliesApp
from wallies.core.config import app_config

__name__ = "Wallies"
__version__ = "0.1.0"

logging.basicConfig(
    level=getattr(logging, environ.get("WALLIES_LOG_LEVEL", "INFO")),
    format="%(filename)s %(message)s",
    datefmt="WALLIES %H:%M:%S",
)


def start():
    cache_dir = app_config.app_dir / "cache"
    if not cache_dir.parent.exists():
        cache_dir.parent.mkdir(parents=True)
    Cachable.register(app_config.get(
        "redis", {}).get("url"), cache_dir.as_posix())
    try:
        app = WalliesApp()
        threads = app.threads
        app.run()
    except KeyboardInterrupt:
        for th in threads:
            try:
                th.stop()
            except:
                pass