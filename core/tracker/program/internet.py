import core.tracker.program.browsers as browsers

from core.tracker.program import BaseProgram
from core.tools import Job


class Internet(BaseProgram):

    def __init__(self, job: Job):
        super().__init__(job)

    @property
    def job(self):
        browser = self._job.program.capitalize()
        if hasattr(browsers, browser):
            return getattr(browsers, browser)(self._job).job
        return self._job
