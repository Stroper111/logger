from abc import ABC, abstractmethod

from core.tools import Job


class AbstractProgram(ABC):
    _job: Job

    @abstractmethod
    def __init__(self, job: Job):
        pass

    @property
    @abstractmethod
    def job(self):
        pass
