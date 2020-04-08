import datetime

from typing import Dict, Union, List

from core.tools import Job
from core.tracker import Tracker


class Session:
    def __init__(self):
        self._current_job: Union[Job, None] = None
        self._activities: Dict[str, Dict[str, List[Dict]]] = dict()
        self._tracker: Tracker = Tracker()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._store_job()
        self.print()

    @property
    def active_job(self):
        return self._current_job

    @property
    def current_time(self):
        return datetime.datetime.now().isoformat(sep='_')

    def run(self):
        if self._current_job is None:
            self._current_job = self._tracker.retrieve_job

        if self._current_job.window_name != self._tracker.active_window_name:
            self._store_job()
            self._current_job = self._tracker.retrieve_job

    def print(self):
        """ Gives a nice print of the current activity list and total time spent on every task and program.  """
        for task, programs in self._activities.items():
            for program, timers in programs.items():
                timer = str(datetime.timedelta(seconds=sum(timer['duration'].seconds for timer in timers)))
                print(f"\nTask: {task}\n\tProgram: {program}\n\t\tTime spend: {timer}")

    def _store_job(self):
        """ Store the current job in the activity list.  """
        self._current_job.stop()

        # Get the task location
        exists_task = self._activities.get(self._current_job.task, None)
        if exists_task  is None:
            self._activities[self._current_job.task] = dict()
            exists_task  = self._activities[self._current_job.task]

        # Get the program location
        exists_program = exists_task .get(self._current_job.program, None)
        if exists_program is None:
            self._activities[self._current_job.task][self._current_job.program] = [self._current_job.timers]
        else:
            self._activities[self._current_job.task][self._current_job.program].append(self._current_job.timers)

    def _create_session(self):
        pass
