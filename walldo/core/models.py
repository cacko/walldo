from enum import StrEnum
from walldo.ui.models import Icon


class Category(StrEnum):
    MINIMAL = "minimal"
    ABSTRACT = "abstract"
    LANDSCAPE = "landscape"
    SPORT = "sport"
    GAMES = "games"
    CARTOON = "cartoon"
    FANTASY = "fantasy"
    NATURE = "nature"
    HORROR = "horror"
    WHATEVER = "whatever"

    @classmethod
    def values(cls):
        return [member.value for member in cls.__members__.values()]


class Command(StrEnum):
    CHANGE_NOW = "change_now"
    CATEGORY = "category"
    INTERVAL = "interval"
    QUIT = "quit"


INTERVAL_OPTIONS = [
    (10, '10 minutes', Icon.MINUTES_10),
    (30, '30 minutes', Icon.MINUTES_30),
    (60, 'Each hour', Icon.EACH_HOUR),
    (1440, 'Every day', Icon.EVERY_DAY),
    (-1, 'Off', Icon.AUTO_CHANGE_OFF),
]
