from typing import Any, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.job import Job
from pytz import utc
from queue import Queue

from walldo.core.models import Command


class scheduler_meta(type):

    __instance: Optional['Scheduler'] = None
    __jobstore: Optional[MemoryJobStore] = None
    manager: Queue

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwds)
        return cls.__instance

    def register(cls, manager_queue: Queue):
        cls.manager = manager_queue

    @property
    def jobstore(cls) -> MemoryJobStore:
        if not cls.__jobstore:
            cls.__jobstore = MemoryJobStore()

        return cls.__jobstore

    def start(cls):
        cls().do_start()

    def set_interval(cls, interval: int):
        cls().do_set_interval(interval)

    @property
    def next_time(cls):
        return cls().get_next_time()


class Scheduler(object, metaclass=scheduler_meta):
    def __init__(self) -> None:
        self.__scheduler = BackgroundScheduler(
            jobstores={
                **dict(default=self.__class__.jobstore)
            },
            job_defaults={
                **dict(
                    coalesce=False,
                    max_instances=1
                )
            },
            timezone=utc
        )

    @property
    def scheduler(self) -> BackgroundScheduler:
        return self.__scheduler

    def push_check_now(self):
        self.__class__.manager.put_nowait((Command.CHANGE_NOW, None))

    def do_set_interval(self, interval: int):
        if interval < 0:
            self.__scheduler.remove_all_jobs()
            return
        self.__scheduler.add_job(
            trigger='interval',
            minutes=interval,
            replace_existing=True,
            coalesce=True,
            func=self.push_check_now,
            id="walldo"
        )

    def get_next_time(self):
        try:
            job = self.__scheduler.get_job("walldo")
            assert job
            assert isinstance(job, Job)
            return job.next_run_time
        except AssertionError:
            return None

    def do_start(self):
        self.__scheduler.start()
