import logging
from os import environ
from wallies.ui.app import WalliesApp
from wallies.config import Config as app_config

__name__ = "Wallies"
__version__ = "0.1.0"

logging.basicConfig(
    level=getattr(logging, environ.get("WALLIES_LOG_LEVEL", "INFO")),
    format="%(filename)s %(message)s",
    datefmt="WALLIES %H:%M:%S",
)


def start():
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