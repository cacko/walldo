from enum import StrEnum


class Category(StrEnum):
    MINIMAL = "minimal"
    ABSTRACT = "abstract"
    MOVIES = "movies"
    SPORT = "sport"
    GAMES = "games"
    CARTOON = "cartoon"
    FANTASY = "fantasy"
    NATURE = "nature"
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
    (10, '10 minutes'),
    (30, '30 minutes'),
    (60, 'Each hour'),
    (1440, 'Every day'),
    (-1, 'Off'),
]
