import logging
from queue import Queue
from wallies.core.models import Command
from wallies.core.macos import get_screen, set_wallpapper
from wallies.api.artwork import ArtworkFile
from wallies.api.client import Client
from wallies.core.thread import StoppableThread
from random import choice
import time


class Manager(StoppableThread):

    app_callback = None
    player_callback = None
    commander: Queue
    __running = False

    def __init__(self, app_callback) -> None:
        self.api = Client()
        self.commander = Queue(maxsize=10)
        self.app_callback = app_callback
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
            cmd, _ = self.commander.get_nowait()
            self.commander.task_done()
            match(cmd):
                case Command.RANDOM:
                    self.__random()
        except Exception as e:
            logging.exception(e)

    def __random(self):
        artworks = self.api.artworks()
        for screen in get_screen():
            raw_src = choice(artworks).raw_src
            artwork_file = ArtworkFile(raw_src)
            artwork_path = artwork_file.path
            res, err = set_wallpapper(screen=screen, image_path=artwork_path)
            logging.debug(res)
            if err:
                logging.error(err)
