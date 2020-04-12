import re

from core.tools import Job
from core.tracker.program import BaseProgram


class Programming(BaseProgram):

    def __init__(self, job: Job):
        super().__init__(job)

    @property
    def job(self):
        specification = self._parser(self._job.window_name)
        self._job.program = f"{self._job.program} ({specification})"
        return self._job

    def _parser(self, window_name):
        specification = window_name.split(' ').pop(0)
        if len(specification.split("/") )> 1:
            return "Unknown"
        return specification
