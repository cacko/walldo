import logging
from typing import Optional
from datetime import datetime, timedelta, timezone
from walldo.config import app_config


class TimerMeta(type):

    __instance: Optional['Timer'] = None

    def __call__(self, *args, **kwds):
        if not self.__instance:
            self.__instance = type.__call__(
                self, app_config.ui_config.interval, *args, **kwds)
        return self.__instance

    @property
    def enabled(cls) -> bool:
        return cls().is_enabled

    @property
    def next_time(cls) -> datetime:
        return cls().time_to_next

    def set_interval(cls, value: int):
        return cls().do_set_interval(value)

    def process(cls) -> bool:
        return cls().do_process()


class Timer(object, metaclass=TimerMeta):

    __next_scheduled: datetime
    __interval: timedelta
    __started: datetime

    def __init__(self, interval: int):
        self.__started = datetime.now(tz=timezone.utc)
        self.__interval = timedelta(minutes=interval)
        logging.debug("init interval=%s", self.__interval)
        self.__next_scheduled = self.__started
        self.__next_scheduled = self.__get_next()
        logging.debug("init next scheduled=%s", self.__next_scheduled)

    @property
    def is_enabled(self) -> bool:
        return self.__interval.total_seconds() > 0

    @property
    def time_to_next(self) -> datetime:
        return self.__next_scheduled

    def __get_next(self):
        seconds = self.__interval.total_seconds()
        result = self.__next_scheduled
        match seconds:
            case 3600:
                st = self.__next_scheduled.replace(minute=0, second=0)
                result = st + self.__interval
            case 86400:
                st = self.__next_scheduled.replace(hour=0, minute=0, second=0)
                result = st + self.__interval
            case _:
                result = self.__next_scheduled + self.__interval
        return result

    def do_set_interval(self, value: int):
        self.__interval = timedelta(minutes=value)
        self.__next_scheduled = self.__get_next()

    def do_process(self) -> bool:
        if not self.is_enabled:
            return False
        result = self.__next_scheduled < datetime.now(tz=timezone.utc)
        if result:
            self.__next_scheduled = self.__get_next()
        return result
