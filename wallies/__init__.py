import logging
from os import environ
from wallies.ui.app import WalliesApp
from wallies.config import app_config

__name__ = "Wallies"

logging.basicConfig(
    level=getattr(logging, environ.get("WALLIES_LOG_LEVEL", "INFO")),
    format="%(filename)s %(message)s",
    datefmt="WALLIES %H:%M:%S",
)


def start():
    try:
        app = WalliesApp()
        threads = app.threads
        print(app_config.get("ui.interval"))
        app.run()
    except KeyboardInterrupt:
        for th in threads:
            try:
                th.stop()
            except:
                pass