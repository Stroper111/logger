import win32gui

import pathlib
import yaml
import time
import os
import re

from core.tracker.abstract import AbstractTracker
from core.tools import Job


class Tracker(AbstractTracker):

    _programs = ('programs', 'programs.yaml')
    _patterns = ('patterns', 'patterns.yaml')

    def __init__(self):
        super().__init__()

        # Get base path
        dir_data = str(pathlib.Path(__file__).parents[2])

        # Predefine for convenience
        self.data_programs: dict = dict()
        self.data_patterns: dict = dict()

        # Get data
        for name, path in [self._programs, self._patterns]:
            full_path = os.path.join(dir_data, "data", path)
            setattr(self, 'data_' + name, self._load_yaml(full_path))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, KeyboardInterrupt):
            print("\n\nProgram terminated by KeyBoard interrupt")
            return True

        if exc_tb:
            print("\n\nUnknown error occurred")
            return False

        print("\n\nProgram terminated successful")

    @property
    def active_window_name(self) -> str:
        window = win32gui.GetForegroundWindow()
        window_name = win32gui.GetWindowText(window)
        return window_name

    @property
    def retrieve_job(self) -> Job:
        """ Return the general information about the info link.  """
        window_name = self.active_window_name

        # Primary attempt to distinguish program
        *info, program_name = window_name.split(" - ")

        # Check for primary programs
        if program_name:
            job: Job = Job(*self._retrieve_program(program_name), window_name)

        # If there is no program name or not found, try pattern matching.
        if not program_name or (program_name and job.task is None):
            job = Job(*self._retrieve_pattern(window_name), window_name)

        # No match found
        if job.task is None:
            job = Job(task='idle', program='unknown', window_name=window_name)
        return job

    @property
    def pycharm(self) -> str:
        window_name = self.active_window_name
        project = window_name.split(" ").pop(0)
        return "Pycharm project: " + project

    @staticmethod
    def _load_yaml(path):
        """ Open a yaml file and return the data.  """
        with open(path) as file:
            data = yaml.safe_load(file)
        return data

    def _retrieve_program(self, program_name):
        """ Get the specific taks and program from a program name.  """
        for task, program in self.data_programs.items():
            if program.get(program_name, None) is not None:
                return task, program[program_name]
        return None, None

    def _retrieve_pattern(self, window_name):
        """ Get the specific taks and program by means of pattern matching.  """
        for task, patterns in self.data_patterns.items():
            for pattern, program in patterns.items():
                if len(re.findall(pattern, window_name)) > 0:
                    return task, program
        return None, None
