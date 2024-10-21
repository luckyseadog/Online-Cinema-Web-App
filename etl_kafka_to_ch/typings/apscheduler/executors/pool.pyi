"""
This type stub file was generated by pyright.
"""

from abc import abstractmethod
from apscheduler.executors.base import BaseExecutor

class BasePoolExecutor(BaseExecutor):
    @abstractmethod
    def __init__(self, pool) -> None: ...
    def shutdown(self, wait=...):  # -> None:
        ...

class ThreadPoolExecutor(BasePoolExecutor):
    """
    An executor that runs jobs in a concurrent.futures thread pool.

    Plugin alias: ``threadpool``

    :param max_workers: the maximum number of spawned threads.
    :param pool_kwargs: dict of keyword arguments to pass to the underlying
        ThreadPoolExecutor constructor
    """

    def __init__(self, max_workers=..., pool_kwargs=...) -> None: ...

class ProcessPoolExecutor(BasePoolExecutor):
    """
    An executor that runs jobs in a concurrent.futures process pool.

    Plugin alias: ``processpool``

    :param max_workers: the maximum number of spawned processes.
    :param pool_kwargs: dict of keyword arguments to pass to the underlying
        ProcessPoolExecutor constructor
    """

    def __init__(self, max_workers=..., pool_kwargs=...) -> None: ...
