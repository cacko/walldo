from typing import Optional, Callable
from rumps import Menu, MenuItem
from rumps import App
from pydantic import BaseModel, Extra
from walldo.ui.models import Icon


class Option(BaseModel, extra=Extra.ignore):
    text: str
    value: int
    icon: Optional[Icon] = None


class OptionItem(BaseModel, extra=Extra.ignore):
    option: Option
    callback: Callable
    dimensions: Optional[tuple[int, int]] = None
    template: bool = True

    @property
    def menu_args(self):
        return dict(
            title=self.option.text,
            callback=self.callback,
            dimensions=self.dimensions,
            template=self.template
        )


class OptionMenuItem(MenuItem):

    def __init__(self, item: OptionItem):
        super().__init__(**item.menu_args)


class OptionList:

    app: App
    menu_key: str
    callback: Callable

    def __init__(self, app: App, menu_key: str, callback: Callable) -> None:
        self.app = app
        self.menu_key = menu_key
        self.callback = callback
        self.__post_init__()

    def __post_init__(self):
        pass

    @property
    def menu(self) -> Menu:
        assert self.app
        return self.app.menu.get(self.menu_key)

    def update(self, options: list[Option]):
        if len(self.menu.keys()):
            self.menu.clear()
        menu = []
        for option in options:
            item = OptionMenuItem(OptionItem(
                option=option, callback=self.callback))
            menu.append(item)
        self.menu.update(menu)
        self.menu._menuitem.setEnabled_(True)

    def reset(self):
        for key in self.menu.keys():
            self.menu.pop(key)

    def set_enabled_value(self, value: str):
        for key, menu_item in self.menu.items():
            menu_item.state = int(key == value)

    def title_to_value(self, title: str) -> int:
        raise NotImplementedError
