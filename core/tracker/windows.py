
from core.tracker.base import BaseTracker
from core.tracker import program
from core.tools import Job, TimeOut


class Tracker(BaseTracker):



    def __init__(self):
        super().__init__()
        
        # Timeout function to retrieve program names.
        self.timout = TimeOut()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def active_window_name(self) -> str:
        return self.timout.active_window

    @property
    def retrieve_job(self) -> Job:
        """ Return the general information about the info link.  """
        window_name = self.active_window_name

        # Primary attempt to distinguish program
        *info, program_name = window_name.split(" - ")

        # Check for primary programs
        if program_name:
            job: Job = self._retrieve_program(program_name, window_name)

        # If there is no program name or not found, try pattern matching.
        if not program_name or (program_name and job.task is None):
            job = self._retrieve_pattern(window_name)

        # Check if we can specify the activity more
        if job.task and hasattr(program, job.task):
            program_filter = getattr(program, job.task)(job)
            job = program_filter.job

        return job
