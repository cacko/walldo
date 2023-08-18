import logging
from traceback import print_exc
import rumps
from walldo.config import app_config
from walldo.core.manager import Manager
from walldo.ui.menu.categories import CategoryList
from .menu.interval import IntervalList
from .menu.option import OptionMenuItem
from walldo.ui.models import (
    ActionItem,
    Icon,
    Label
)
from walldo.core.models import Command
from corethread import StoppableThread
from walldo.ui.menu.timer import TimerItem


class WalliesAppMeta(type):

    _instance = None

    def __call__(cls, *args, **kwds):
        if not cls._instance:
            cls._instance = type.__call__(cls, *args, **kwds)
        return cls._instance

    def quit(cls):
        cls().terminate()


class WalldoApp(rumps.App, metaclass=WalliesAppMeta):

    __threads: list[StoppableThread] = []

    def __init__(self):
        super(WalldoApp, self).__init__(
            name="walldo",
            menu=[
                TimerItem.time_left,
                ActionItem.change_now,
                None,
                ActionItem.category,
                ActionItem.interval,
                None,
                ActionItem.quit
            ],
            icon=Icon.APP.value,
            quit_button=None,
            template=True,

        )
        self.menu.setAutoenablesItems = False
        TimerItem.time_left.setAvailability(True)
        self.__intervals = IntervalList(
            self,
            Label.INTERVAL.value,
            self.onIntervalItem
        )
        self.__category = CategoryList(
            self,
            Label.CATEGORY.value,
            self.onCategoryItem
        )
        self.manager = Manager(self.onManagerResult)
        self.manager.start()
        self.__threads.append(self.manager)
        logging.info("App loaded")
        self.__intervals.set_enabled_value(app_config.ui_config.interval_text)
        self.__category.set_enabled_value(app_config.ui_config.category.value)

    @property
    def threads(self):
        return self.__threads

    @rumps.events.on_menu_open
    def menu_open(self):
        TimerItem.time_left.self_update()

    @rumps.clicked(Label.CHANGE_NOW.value)
    def onChangeNow(self, sender):
        self.manager.commander.put_nowait((Command.CHANGE_NOW, None))

    def onIntervalItem(self, sender: OptionMenuItem):
        interval_value = self.__intervals.title_to_value(sender.title)
        self.__intervals.set_enabled_value(sender.title)
        self.manager.commander.put_nowait((Command.INTERVAL, interval_value))

    def onCategoryItem(self, sender: OptionMenuItem):
        category = sender.title
        self.__category.set_enabled_value(category)
        self.manager.commander.put_nowait((Command.CATEGORY, category))

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
