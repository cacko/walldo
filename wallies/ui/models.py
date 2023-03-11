from rumps import MenuItem
from enum import Enum, StrEnum


class Categories(StrEnum):
    MINIMAL = "minimal"
    ABSTRACT = "abstract"
    MOVIES = "movies"
    SPORT = "sport"
    MUSIC = "music"
    GAMES = "games"
    CARTOON = "cartoon"
    COLOURS = "colours"
    FANTASY = "fantasy"
    NATURE = "nature"
    WHATEVER = "whatever"


class Label(Enum):
    QUIT = 'Quit'
    RANDOM = 'Random'
    INTERVAL = 'Auto change'


class Icon(Enum):
    QUIT = 'power'
    RANDOM = 'dice'
    APP = 'photo.stack'
    INTERVAL = "timer"
    INTERVAL_10 = "10.circle"
    INTERVAL_30 = "30.circle"
    INTERVAL_60 = "hourglass.circle"
    INTERVAL_1440 = "calendar.circle"


INTERVAL_OPTIONS = [
    (10, '10 minutes', Icon.INTERVAL_10),
    (30, '30 minutes', Icon.INTERVAL_30),
    (60, 'Each hour', Icon.INTERVAL_60),
    (1440, 'Every day', Icon.INTERVAL_1440),
]


class ActionItemMeta(type):

    _instances: dict[str, 'ActionItem'] = {}

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

    def __init__(
        self,
        title,
        callback=None,
        key=None,
        icon=None,
        dimensions=None,
        template=None
    ):
        template = True
        super().__init__(title, callback, key, icon, dimensions, template)

    def setAvailability(self, enabled: bool):
        self._menuitem.setEnabled_(enabled)
