import logging
import os
import corelog
from walldo.ui.app import WalldoApp
import signal
import sys

__name__ = "Walldo"

log_level = os.environ.get("WALLDO_LOG_LEVEL", "DEBUG")
corelog.register(log_level=log_level)


def start():
    app = WalldoApp()

    def handler_stop_signals(signum, frame):
        app.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, handler_stop_signals)
    signal.signal(signal.SIGTERM, handler_stop_signals)
    try:
        app.run()
        app.terminate()
    except KeyboardInterrupt:
        app.template()
    except Exception as e:
        logging.exception(e)
