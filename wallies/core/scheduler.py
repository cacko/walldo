import logging
from typing import Optional
from wallies.config import app_config
from wallies.core.thread import StoppableThread
from .models import Command
from apscheduler.schedulers.blocking import BlockingScheduler
from pathlib import Path
from queue import Queue
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class SchedulerMeta(type):

    __instance: Optional['Scheduler'] = None
    __manager: Optional[Queue] = None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwargs)
        return cls.__instance

    def invoke(cls, manager: Queue) -> 'Scheduler':
        cls.__manager = manager
        cls().start()
        return cls()

    @property
    def manager(cls) -> Optional[Queue]:
        return cls.__manager

    @property
    def db_path(cls) -> Path:
        return app_config.data_dir / "scheduler.sqlite"

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

    def __init__(self):
        scheduler = BlockingScheduler()
        url = f"sqlite:///{Scheduler.db_path.as_posix()}"
        logging.info(url)
        scheduler.add_jobstore(SQLAlchemyJobStore(url=url))
        self.__scheduler = scheduler
        super().__init__()

    def run(self) -> None:
        self.__scheduler.start()
        return super().run()

    def add_job(self,  **kwargs):
        return self.__scheduler.add_job(**kwargs)
