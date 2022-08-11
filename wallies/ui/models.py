from rumps import MenuItem
from pathlib import Path
from enum import Enum


class Label(Enum):
    QUIT = 'Quit'
    RANDOM = 'Random'
    INTERVAL = 'Auto change'


class Icon(Enum):
    QUIT = 'quit.png'
    RANDOM = 'random.png'
    APP = 'app.png'
    INTERVAL = "interval.png"
    INTERVAL_10 = "10.png"
    INTERVAL_30 = "30.png"
    INTERVAL_60 = "60.png"
    INTERVAL_1440 = "1440.png"

    def __new__(cls, *args):
        icons_path: Path = Path(__file__).parent / "icons"
        value = icons_path / args[0]
        obj = object.__new__(cls)
        obj._value_ = value.as_posix()
        return obj


INTERVAL_OPTIONS = [
    (10, '10 minutes', Icon.INTERVAL_10),
    (30, '30 minutes', Icon.INTERVAL_30),
    (60, 'Each hour', Icon.INTERVAL_60),
    (1440, 'Every day', Icon.INTERVAL_1440),
]


class ActionItemMeta(type):

    _instances = {}

    def __call__(cls, name, *args, **kwds):
        if name not in cls._instances:
            cls._instances[name] = super().__call__(*args, **kwds)
        return cls._instances[name]

    @property
    def quit(cls) -> 'ActionItem':
        return cls("quit", Label.QUIT.value, icon=Icon.QUIT.value)

    @property
    def random(cls) -> 'ActionItem':
        return cls("random", Label.RANDOM.value, icon=Icon.RANDOM.value)

    @property
    def interval(cls) -> 'ActionItem':
        return cls("interval", Label.INTERVAL.value, icon=Icon.INTERVAL.value)


class ActionItem(MenuItem, metaclass=ActionItemMeta):

    def __init__(self, title, callback=None, key=None, icon=None, dimensions=None, template=None):
        template = True
        super().__init__(title, callback, key, icon, dimensions, template)

    def setAvailability(self, enabled: bool):
        self._menuitem.setEnabled_(enabled)
