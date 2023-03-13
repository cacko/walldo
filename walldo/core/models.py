from enum import StrEnum


class Category(StrEnum):
    MINIMAL = "minimal"
    ABSTRACT = "abstract"
    MOVIES = "movies"
    SPORT = "sport"
    MUSIC = "music"
    GAMES = "games"
    CARTOON = "cartoon"
    COLOURS = "colours"
    FANTASY = "fantasy"
    NATURE = "nature"
    WHATEVER = "whatever"

    @classmethod
    def values(cls):
        return [member.value for member in cls.__members__.values()]


class Source(StrEnum):
    WEB = "web"
    MASHA = "masha"

    @classmethod
    def values(cls):
        return [member.value for member in cls.__members__.values()]


class Command(StrEnum):
    CHANGE_NOW = "change_now"
    CATEGORY = "category"
    INTERVAL = "interval"
    QUIT = "quit"
    SOURCE = "source"


INTERVAL_OPTIONS = [
    (10, '10 minutes'),
    (30, '30 minutes'),
    (60, 'Each hour'),
    (1440, 'Every day'),
    (-1, 'Off'),
]
