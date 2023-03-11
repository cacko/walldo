import logging
from traceback import print_exc
from typing import Optional
import rumps
from ..core.scheduler import Scheduler
from wallies.core.thread import StoppableThread
from wallies.core.manager import Manager
from .menu.interval import IntervalList, Option
from wallies.ui.models import INTERVAL_OPTIONS, ActionItem, Icon, Label
from wallies.core.models import Command


class WalliesAppMeta(type):

    _instance = None

    def __call__(cls, *args, **kwds):
        if not cls._instance:
            cls._instance = type.__call__(cls, *args, **kwds)
        return cls._instance

    def quit(cls):
        cls().terminate()


class WalliesApp(rumps.App, metaclass=WalliesAppMeta):

    manager: Optional[Manager] = None
    __threads: list[StoppableThread] = []
    __intervals: Optional[IntervalList] = None

    def __init__(self):
        super(WalliesApp, self).__init__(
            name="Wallies",
            menu=[
                ActionItem.random,
                ActionItem.interval,
                None,
                ActionItem.quit
            ],
            icon=Icon.APP.value,
            quit_button=None,
            template=True,

            nosleep=True,

        )
        self.menu.setAutoenablesItems = False
        self.__intervals = IntervalList(self, Label.INTERVAL.value)
        self.manager = Manager(self.onManagerResult)
        self.manager.start()
        self.__threads.append(self.manager)

        self.__threads.append(Scheduler.invoke(self.manager.commander))
        self.__intervals.update(
            [Option(text=t, value=v, icon=i) for v, t, i in INTERVAL_OPTIONS],
            self.onIntervalItem
        )
        logging.info("App")

    @property
    def threads(self):
        return self.__threads

    @rumps.clicked(Label.RANDOM.value)
    def onRandom(self, sender):
        self.manager.commander.put_nowait((Command.RANDOM, None))

    def onIntervalItem(self, sender):
        print(sender)

    @rumps.clicked(Label.QUIT.value)
    def onQuit(self, sender):
        self.terminate()

    @rumps.events.on_screen_sleep
    def sleep(self):
        pass

    @rumps.events.on_screen_wake
    def wake(self):
        pass

    def onManagerResult(self, resp):
        method = f"_on{resp.__class__.__name__}"
        if hasattr(self, method):
            getattr(self, method)(resp)

    @rumps.events.before_quit
    def terminate(self):
        self.manager.commander.put_nowait((Command.QUIT, None))
        for th in self.__threads:
            try:
                th.stop()
            except Exception:
                pass
        try:
            rumps.quit_application()
        except Exception as e:
            print_exc(e)
