import logging
from queue import Queue
from walldo.api.models import Artwork
from walldo.core.models import Command
from walldo.core.macos import get_screen, set_wallpapper
from walldo.api.artwork import ArtworkFile
from walldo.api.client import Client
from corethread import StoppableThread
from walldo.core.scheduler import Scheduler
from walldo.config import app_config
import time


class Manager(StoppableThread):

    app_callback = None
    player_callback = None
    commander: Queue
    __running = False
    __artworks: list[Artwork] = []

    def __init__(self, app_callback) -> None:
        self.api = Client()
        self.commander = Queue(maxsize=10)
        self.app_callback = app_callback
        assert app_config.ui_config.interval
        Scheduler.register(self.commander)
        Scheduler.set_interval(app_config.ui_config.interval)
        Scheduler.start()
        super().__init__()

    def run(self):
        self.__running = True
        while self.__running:
            if self.commander.empty():
                time.sleep(0.1)
                continue
            self.commander_runner()

    def commander_runner(self):
        try:
            cmd, payload = self.commander.get_nowait()
            self.commander.task_done()
            match(cmd):
                case Command.CHANGE_NOW:
                    self.__change_now()
                case Command.INTERVAL:
                    self.__interval(payload)
                case Command.CATEGORY:
                    self.__category(payload)
        except Exception as e:
            logging.exception(e)

    def __change_now(self):
        for screen in get_screen():
            if not len(self.__artworks):
                self.__artworks = self.api.artworks(
                    category=app_config.ui_config.category
                )
            raw_src = self.__artworks.pop(0).raw_src
            logging.warning(self.__artworks)
            artwork_file = ArtworkFile(raw_src)
            artwork_path = artwork_file.path
            res, err = set_wallpapper(screen=screen, image_path=artwork_path)
            logging.debug(res)
            if err:
                logging.error(err)

    def __interval(self, interval_value: int):
        app_config.set(var="ui.interval", value=interval_value)
        Scheduler.set_interval(interval_value)

    def __category(self, category: str):
        self.__artworks = []
        app_config.set(var="ui.category", value=category.lower())
