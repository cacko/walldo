from .option import OptionList, Option
from walldo.core.models import Category


class CategoryList(OptionList):

    def __post_init__(self):
        self.update(
            [Option(text=t, value=v)
             for v, t in enumerate(Category.values(), start=100)]
        )
