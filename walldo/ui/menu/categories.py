from .option import OptionList, Option
from walldo.core.models import Category
from walldo.ui.models import Icon


class CategoryList(OptionList):

    def __post_init__(self):
        self.update(
            [Option(text=t, value=v, icon=Icon[f"CATEGORY_{t.upper()}"])
             for v, t in enumerate(Category.values(), start=100)]
        )
