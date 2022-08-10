import logging
from queue import Queue
import asyncio
from wallies.core.models import Command

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
    api = None
    __running = False

    def __init__(self) -> None:
        self.eventLoop = asyncio.new_event_loop()
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
        pass