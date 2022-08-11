from dataclasses import dataclass
from typing import Optional
from dataclasses_json import dataclass_json, Undefined
from rumps import Menu, MenuItem
from rumps import App
from AppKit import NSAttributedString
from textwrap import wrap
from wallies.ui.models import Icon


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Option:
    text: str
    value: int
    icon: Optional[Icon] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OptionItem:
    option: Option
    callback: callable
    dimensions: Optional[tuple[int, int]] = None
    template: bool = True

    @property
    def menu_args(self):
        return {
            "title": self.option.text,
            "callback": self.callback,
            "icon": self.option.icon.value if self.option.icon else None,
            "dimensions": self.dimensions,
            "template": self.template
        }


class OptionMenuItem(MenuItem):

    def __init__(self, item: OptionItem):
        super().__init__(**item.menu_args)


class OptionList:

    items: list[OptionItem] = []
    app: App = None
    menu_key: str = None

    def __init__(self, app: App, menu_key: str) -> None:
        self.app = app
        self.menu_key = menu_key

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]

    def __iter__(self):
        return iter(self.items)

    def __reversed__(self):
        return reversed(self.items)

    @property
    def menu(self) -> Menu:
        return self.app.menu.get(self.menu_key)

    def append(self, item: OptionItem):
        self.items.append(item)

    def update(self, options: list[Option], callback):
        if len(self.menu.keys()):
            self.menu.clear()
        menu = []
        for option in options:
            menu.append(OptionMenuItem(
                OptionItem(option=option, callback=callback)
            ))
        self.menu.update(menu)
        self.menu._menuitem.setEnabled_(True)

    def reset(self):
        for item in self.__items:
            self.menu.pop(item.key)


class IntervalList(OptionList):

    pass
