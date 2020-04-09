
from core.tracker.program import BaseProgram
from core.tools import Job


class Firefox(BaseProgram):

    def __init__(self, job: Job):
        super().__init__(job)

    @property
    def job(self):
        return self._job

    def parser(self, name):
        """ Returns the base name of the program based on the window name.  """
        """ 
        # Github
        'Stroper111'

        # Pommerman, Education
        Projects · Dashboard · GitLab - Mozilla Firefox
        'Education / '   - 'Gitlab'

        # YouTube - Mozilla Firefox

        # LoL Esports - Mozilla Firefox

        # Netflix - Mozilla Firefox

        # WhatsApp - Mozilla Firefox

        """
