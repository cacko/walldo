from .option import OptionList, Option
from walldo.core.models import Source


class SourceList(OptionList):

    def __post_init__(self):
        self.update(
            [Option(text=t, value=v)
             for v, t in enumerate(Source.values(), start=100)]
        )
