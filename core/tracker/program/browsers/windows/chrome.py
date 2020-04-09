from core.tracker.program import BaseProgram
from core.tools import Job


class Chrome(BaseProgram):

    def __init__(self, job: Job):
        super().__init__(job)

    @property
    def job(self):
        return self._job
