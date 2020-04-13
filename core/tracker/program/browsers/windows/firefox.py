import re

from core.tracker.program import BaseProgram
from core.tools import Job


class Firefox(BaseProgram):

    def __init__(self, job: Job):
        super().__init__(job)

    @property
    def job(self):
        specification = self._parser(self._job._window_name)
        if specification is not None:
            self._job.program = f"{self._job.program} ({specification})"
        return self._job

    def _parser(self, window_name: str):
        """ Returns the base name of the program based on the window name.  """

        # Special case
        if window_name.endswith("Mozilla Firefox (Private Browsing)"):
            self._job._window_name = 'hidden'
            return None

        methods = ['_startswith', '_endswith', '_pattern', '_splitting']
        for method in methods:
            specific = getattr(self, method)(window_name)
            if isinstance(specific, str):
                return specific
        # No specification found
        return None

    @staticmethod
    def _startswith(window_name):
        """ Filter out all startswith.  """
        starts = {"Stroper111": 'Github',
                  "jMonkeyEngine 3": 'JME'}
        for key, value in starts.items():
            if window_name.startswith(key):
                return value
        return None

    @staticmethod
    def _endswith(window_name):
        """ Filter out all endswith.  """
        ends = {"GitLab - Mozilla Firefox": 'GitLab'}
        for key, value in ends.items():
            if window_name.endswith(key):
                return value
        return None

    @staticmethod
    def _pattern(window_name):
        patterns = {"WhatsApp .* Mozilla Firefox": 'WhatsApp',
                    ".* ULTIMATE GUITAR TABS - .*": 'Guitar',
                    ".* Ultimate-Guitar.Com": 'Guitar',
                    "Y\d Q\d - .* - Online LaTeX Editor Overleaf": 'unie',
                    "[\d\w]{6} - .* - Online LaTeX Editor Overleaf": 'unie',
                    "https://www.youtube.com/watch.*": 'Youtube',
                    }
        for key, value in patterns.items():
            if len(re.findall(key, window_name)) > 0:
                return value
        return None

    @staticmethod
    def _splitting(window_name):
        """ Left over attempt to just break up the name, by last two sections.  """

        # YouTube - Mozilla Firefox
        # LoL Esports - Mozilla Firefox
        # Netflix - Mozilla Firefox
        window = window_name.split(" - ")
        if len(window) == 2 and len(window[0]) < 20 and window[0] != window[1]:
            return window[0]

        if len(window) > 2 and len(window[-2]) < 20 and window[-2] != window[-1]:
            return window[-2]

        return None