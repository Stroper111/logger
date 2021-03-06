from core.tracker.program import AbstractProgram
from core.tools import Job


class BaseProgram(AbstractProgram):

    def __init__(self, job: Job):
        super().__init__(job)

        self._job = job

    @property
    def job(self):
        return self._job

