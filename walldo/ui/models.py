from rumps import MenuItem
from enum import StrEnum


class Label(StrEnum):
    QUIT = 'Quit'
    CHANGE_NOW = 'Change now'
    CATEGORY = 'Category'
    INTERVAL = 'Auto change'
    SOURCE = "Source"


class Icon(StrEnum):
    QUIT = 'power'
    CHANGE_NOW = 'photo.on.rectangle.angled'
    APP = 'photo.stack.fill'
    CATEGORY = 'list.clipboard'
    INTERVAL = "timer"
    SOURNCE = "hammer.fill"


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

    @property
    def source(cls) -> 'ActionItem':
        return cls("source", Label.SOURCE.value, icon=Icon.SOURNCE.value)


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
