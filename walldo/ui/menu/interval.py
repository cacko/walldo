from .option import OptionList, Option
from walldo.core.models import INTERVAL_OPTIONS


class IntervalList(OptionList):

    def __post_init__(self):
        self.update(
            [Option(text=t, value=v) for v, t in INTERVAL_OPTIONS]
        )
