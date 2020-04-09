from core.tracker.program import BaseProgram
from core.tools import Job


class Tor(BaseProgram):

    def __init__(self, job: Job):
        super().__init__(job)

    @property
    def job(self):
        self._job.window_name = 'hidden'
        return self._job
