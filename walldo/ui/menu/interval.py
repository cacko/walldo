from .option import OptionList, Option
from walldo.core.models import INTERVAL_OPTIONS


class IntervalList(OptionList):

    def __post_init__(self):
        self.update(
            [Option(text=t, value=v) for v, t in INTERVAL_OPTIONS]
        )

    def title_to_value(self, title: str) -> int:
        try:
            result = next(
                filter(lambda x: x[1] == title, INTERVAL_OPTIONS), None)
            assert result
            return result[0]
        except AssertionError:
            return -1
