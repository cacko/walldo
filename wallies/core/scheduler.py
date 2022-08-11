from wallies.config import app_config
from wallies.core.thread import StoppableThread
from .models import Command
from apscheduler.schedulers.blocking import BlockingScheduler
from pathlib import Path
from queue import Queue


class SchedulerMeta(type):

    __instance: 'Scheduler' = None
    __manager: Queue = None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = type.call(cls, *args, **kwargs)
        return cls.__instance

    def start(cls, manager: Queue) -> 'Scheduler':
        cls().run()
        return cls()

    @property
    def manager(cls) -> Queue:
        return cls.__manager

    @property
    def db_path(cls) -> Path:
        return app_config.app_dir / "scheduler.sqlite"

    def add_interval(cls, minutes: int):
        return cls().add_job(
            id="interval",
            name="interval job",
            func=cls.onIntervalJob,
            trigger="interval",
            minutes=1,
            replace_existing=True,
            misfire_grace_time=180
        )

    def onIntervalJob(cls):
        cls.manager.put_nowait((Command.RANDOM, None))


class Scheduler(StoppableThread, metaclass=SchedulerMeta):

    __scheduler: BlockingScheduler() = None

    def __init__(self):
        scheduler = BlockingScheduler()
        url = f"sqlite:///{__class__.db_path.as_posix()}"
        scheduler.add_jobstore("sqlaclhemy", url=url)
        self.__scheduler = scheduler

    def run(self) -> None:
        self.__scheduler.start()
        return super().run()

    def add_job(self,  **kwargs):
        return self.__scheduler.add_job(**kwargs)
