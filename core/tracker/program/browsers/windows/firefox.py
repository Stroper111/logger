import re

from core.tracker.program import BaseProgram
from core.tools import Job


class Firefox(BaseProgram):

    def __init__(self, job: Job):
        super().__init__(job)

    @property
    def job(self):
        specification = self._parser(self._job.window_name)
        if specification is not None:
            self._job.program = f"{self._job.program} ({specification})"
        return self._job

    def _parser(self, window_name: str):
        """ Returns the base name of the program based on the window name.  """

        if window_name.endswith("Mozilla Firefox (Private Browsing)"):
            self._job.window_name = 'hidden'
            return None

        if window_name.startswith("Stroper111"):
            return "Github"

        if window_name.endswith("GitLab - Mozilla Firefox"):
            return "GitLab"

        if len(re.findall("WhatsApp .* Mozilla Firefox")) > 0:
            return 'WhatsApp'

        # YouTube - Mozilla Firefox
        # LoL Esports - Mozilla Firefox
        # Netflix - Mozilla Firefox
        window = window_name.split(" - ")
        if len(window) == 2 and len(window[0]) < 20:
            return window.pop(0)

        # No specification found
        return None
