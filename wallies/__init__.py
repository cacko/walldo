import logging
import os
import corelog
from wallies.ui.app import WalliesApp
import signal
import sys

__name__ = "Wallies"

log_level = os.environ.get("WALLIES_LOG_LEVEL", "DEBUG")
corelog.register(log_level=log_level)


def start():
    try:
        app = WalliesApp()

        def handler_stop_signals(signum, frame):
            app.terminate()
            sys.exit(0)

        signal.signal(signal.SIGINT, handler_stop_signals)
        signal.signal(signal.SIGTERM, handler_stop_signals)

        app.run()
        app.terminate()
        print("app ended")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception(e)
