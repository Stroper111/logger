import datetime
import os
import pathlib

from typing import Dict, Union, List

from core.tools import Job
from core.tracker import Tracker


class Session:
    _format_time = '%Y-%m-%d_%H-%M-%S'
    _dir_activity = 'activities'
    _dir_logs = 'logs.json'

    def __init__(self):
        # Get base path
        dir_logger = str(pathlib.Path(__file__).parents[1])
        self.dir_session = os.path.join(dir_logger, 'data', self._dir_activity, self.current_time)

        # Define trackers
        self._current_job: Union[Job, None] = None
        self._activities: Dict[str, Dict[str, List[Dict]]] = dict()
        self._tracker: Tracker = Tracker()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._current_job is not None:
            self._store_job()
            self._save_summary()
            self.print(threshold=0)
            os.system(f"start {os.path.join(self.dir_session, 'summary.txt')}")

        if isinstance(exc_val, KeyboardInterrupt):
            print("\n\nProgram terminated by KeyBoard interrupt")
            return True

        if exc_tb:
            print("\n\nUnknown error occurred")
            return False

        print("\n\nProgram terminated successful")

    @property
    def active_job(self):
        return self._current_job

    @property
    def current_time(self):
        return datetime.datetime.now().strftime(self._format_time)

    def save_summary(self):
        """ Save a summary of the current activities.  """
        self._save_job()
        self._current_job = self._tracker.retrieve_job
        self._save_summary()

    def run(self):
        if self._current_job is None:
            self._current_job = self._tracker.retrieve_job

        if self._current_job != self._tracker.retrieve_job:
            self._store_job()
            self._current_job = self._tracker.retrieve_job

    def print(self,  threshold=60):
        """ Gives a nice print of the current activity list and total time spent on every task and program.  """
        for task, programs in sorted(self._activities.items()):
            for program, duration in sorted(programs.items()):
                timer = datetime.timedelta(seconds=duration)
                if timer.seconds > threshold:
                    print(f"\nTask: {task}\n\tProgram: {program:30s} duration: {timer}")

    def _store_job(self):
        """ Terminate job, store it to disk and add duration to activity list.  """
        # Terminate the job
        self._current_job.stop()

        # Represent current job
        print(f"\n{self._current_job}")

        # Store the job to a json file.
        self._save_job()

        # Store the job duration in the activity list.
        self.store_duration()

    def store_duration(self):
        """ Store the current job duration in the activity list.  """

        # Get the task location
        exists_task = self._activities.get(self._current_job.task, None)
        if exists_task is None:
            self._activities[self._current_job.task] = dict()
            exists_task = self._activities[self._current_job.task]

        # Get the program location
        exists_program = exists_task.get(self._current_job.program, None)
        if exists_program is None:
            self._activities[self._current_job.task][self._current_job.program] = self._current_job.duration.seconds
        else:
            self._activities[self._current_job.task][self._current_job.program] += self._current_job.duration.seconds

    def _save_job(self):
        """ Store the job to disk.  """
        if not os.path.exists(self.dir_session):
            os.makedirs(self.dir_session)

        path_logs = os.path.join(self.dir_session, 'logs.txt')
        data = self._current_job.serialize
        with open(path_logs, 'a') as file:
            file.write(data + '\n')

    def _save_summary(self):
        if not os.path.exists(self.dir_session):
            os.makedirs(self.dir_session)

        path_summary = os.path.join(self.dir_session, 'summary.txt')
        with open(path_summary, 'a') as file:
            for task, programs in sorted(self._activities.items()):
                file.write(f"\n\nTask: {task}")
                for program, duration in sorted(programs.items()):
                    timer = datetime.timedelta(seconds=duration)
                    file.write(f"\n\tProgram: {program:30s} duration: {timer}")
