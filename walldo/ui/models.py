from rumps import MenuItem
from enum import StrEnum


class Label(StrEnum):
    QUIT = 'Quit'
    CHANGE_NOW = 'Change now'
    CATEGORY = 'Category'
    INTERVAL = 'Auto change'


class Icon(StrEnum):
    QUIT = 'power'
    CHANGE_NOW = 'photo.on.rectangle.angled'
    APP = 'photo.stack.fill'
    CATEGORY = 'list.clipboard'
    INTERVAL = "timer"
    MINUTES_10 = "10.circle.fill"
    MINUTES_30 = "30.circle.fill"
    EACH_HOUR = "hourglass.circle.fill"
    EVERY_DAY = "sunset.fill"
    AUTO_CHANGE_OFF = "livephoto.slash"
    CATEGORY_MINIMAL = "light.min"
    CATEGORY_ABSTRACT = "scribble.variable"
    CATEGORY_LANDSCAPE = "iphone.gen2.landscape"
    CATEGORY_SPORT = "figure.disc.sports"
    CATEGORY_GAMES = "gamecontroller"
    CATEGORY_CARTOON = "highlighter"
    CATEGORY_FANTASY = "highlighter"
    CATEGORY_NATURE = "leaf.fill"
    CATEGORY_HORROR = "eye.trianglebadge.exclamationmark"
    CATEGORY_WHATEVER = "magazine.fill"


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
    def change_now(cls) -> 'ActionItem':
        return cls(
            "change_now",
            Label.CHANGE_NOW.value,
            icon=Icon.CHANGE_NOW.value
        )

    @property
    def interval(cls) -> 'ActionItem':
        return cls("interval", Label.INTERVAL.value, icon=Icon.INTERVAL.value)

    @property
    def category(cls) -> 'ActionItem':
        return cls("category", Label.CATEGORY.value, icon=Icon.CATEGORY.value)


class ActionItem(MenuItem, metaclass=ActionItemMeta):

    def __init__(
        self,
        title: str,
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
