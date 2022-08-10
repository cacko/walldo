import logging
from queue import Queue
import asyncio
from wallies.core.models import Command
from wallies.core.macos import get_screen, set_wallpapper
from wallies.api.artwork import ArtworkFile
from wallies.api.client import Client
from wallies.api.models import Artwork
from random import choice


class ManagerMeta(type):

    _instance = None

    def __call__(self, *args, **kwds):
        if not self._instance:
            self._instance = super().__call__(*args, **kwds)
        return self._instance


class Manager(object, metaclass=ManagerMeta):

    commander: Queue = None
    eventLoop: asyncio.AbstractEventLoop = None
    app_callback = None
    player_callback = None
    api: Client = None
    __running = False

    def __init__(self) -> None:
        self.eventLoop = asyncio.new_event_loop()
        self.api = Client()
        self.commander = Queue()

    def start(self, app_callback):
        self.app_callback = app_callback
        self.__running = True
        tasks = asyncio.wait(
            [self.command_processor()])
        self.eventLoop.run_until_complete(tasks)

    async def command_processor(self):
        while self.__running:
            if self.commander.empty():
                await asyncio.sleep(0.1)
                continue
            await self.commander_runner()

    async def commander_runner(self):
        try:
            cmd, payload = self.commander.get_nowait()
            self.commander.task_done()
            match(cmd):
                case Command.RANDOM:
                    await self.__random()
        except Exception as e:
            logging.exception(e)

    async def __random(self):
        artworks = self.api.artworks()
        for screen in get_screen():
            raw_src = choice(artworks).raw_src
            artwork_file = ArtworkFile(raw_src)
            artwork_path = artwork_file.path
            res, err = set_wallpapper(screen=screen, image_path=artwork_path)
            logging.debug(res)
            if err:
                logging.error(err)
