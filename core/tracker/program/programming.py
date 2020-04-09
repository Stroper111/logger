import re

from core.tools import Job
from core.tracker.program import BaseProgram


class Programming(BaseProgram):

    def __init__(self, job: Job):
        super().__init__(job)

    @property
    def job(self):
        window_name = self._job.window_name
        if len(re.findall(".* [.*] - .*", window_name)) > 0:
            project = window_name.split(" ").pop(0)
            self._job.program = f"{self._job.program} ({project})"
        return self._job
