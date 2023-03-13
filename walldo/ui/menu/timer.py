import logging
from typing import Optional
from rumps import MenuItem
from arrow import Arrow
from walldo.core.timer import Timer


class TimerItemMeta(type):

    _instances: dict[str, 'TimerItem'] = {}

    def __call__(cls, name, *args, **kwds):
        if name not in cls._instances:
            cls._instances[name] = super().__call__(*args, **kwds)
        return cls._instances[name]

    @property
    def time_left(cls) -> 'TimerItem':
        return cls("time_left")


class TimerItem(MenuItem, metaclass=TimerItemMeta):
    def __init__(
        self,
        title: Optional[str] = None
    ):
        template = True
        title = self.get_title()
        super().__init__(title, None, None, None, None, template)

    def setAvailability(self, enabled: bool):
        self._menuitem.setEnabled_(enabled)

    def get_title(cls) -> str:
        if not Timer.enabled:
            return "No autoupdate"
        logging.debug(Timer.next_time)
        fmt = Arrow.fromdatetime(Timer.next_time).humanize(Arrow.utcnow())
        return f"Next {fmt}"

    def self_update(self):
        self.title = self.get_title()
