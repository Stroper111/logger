import datetime
import os
import pathlib
import codecs

from typing import Dict, Union, List

from core.tools import Job
from core.tracker import Tracker


class Session:
    _format_dir = '%Y-%m-%d_%H-%M-%S'
    _format_time = '%Y %b %d, %a %H:%M:%S'
    _dir_activity = 'activities'
    _dir_logs = 'logs.json'

    def __init__(self):
        # Get base path
        dir_logger = str(pathlib.Path(__file__).parents[1])
        self.dir_session = os.path.join(dir_logger, 'data', self._dir_activity, self.current_time())

        # Define trackers
        self._current_job: Union[Job, None] = None
        self._activities: Dict[str, Dict[str, List[Dict]]] = dict()
        self._tracker: Tracker = Tracker()

        # Session trackers
        self._start_time: datetime = datetime.datetime.now()
        self._total_duration: int = 0

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

    def current_time(self, format=None):
        format = self._format_dir if format is None else format
        return datetime.datetime.now().strftime(format)

    def save_summary(self):
        """ Save a summary of the current activities.  """
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

        # Filter out quick Micromanagement
        if (self._current_job.duration.seconds > 2):
            print(f"\n{self._current_job}")
        else:
            print(f"\nMicromanagement: {self._current_job.window_name}")
            self._current_job.task = 'Micromanagement'

        # Store the job to a json file.
        self._save_job()

        # Store the job duration in the activity list.
        self.store_duration()

    def store_duration(self):
        """ Store the current job duration in the activity list.  """
        self._total_duration += self._current_job.duration.seconds

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
        with codecs.open(path_logs, 'a', 'utf-8') as file:
            file.write(data + '\n')

    def _save_summary(self):
        if not os.path.exists(self.dir_session):
            os.makedirs(self.dir_session)

        path_summary = os.path.join(self.dir_session, 'summary.txt')
        with codecs.open(path_summary, 'w', 'utf-8') as file:

            for task, programs in sorted(self._activities.items()):
                file.write(f"\n\nTask: {task}")

                for program, duration in sorted(programs.items()):
                    timer = datetime.timedelta(seconds=duration)
                    file.write(f"\n\tProgram: {program:30s} duration: {timer}")

            file.write(self._save_stats())

    def _save_stats(self):
        passed_seconds = (datetime.datetime.now() - self._start_time).seconds
        total_logged = datetime.timedelta(seconds=self._total_duration)
        total_passed = datetime.timedelta(seconds=passed_seconds)
        percentage = self._total_duration / (passed_seconds if passed_seconds else 1)

        return f"\n\nTotal duration: {total_passed}" \
               f"\n\tLogged      - {str(total_logged):>25s} ({percentage * 100:4.1f}%)" \
               f"\n\tStart time  - {self._start_time.strftime(self._format_time)}" \
               f"\n\tEnd time    - {self.current_time(self._format_time)}"
