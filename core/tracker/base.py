import os
import pathlib
from abc import ABC, abstractmethod

import yaml

from core.tools import Job


class BaseTracker(ABC):
    _programs = ('programs', 'programs.yaml')
    _patterns = ('patterns', 'patterns.yaml')

    @abstractmethod
    def __init__(self):
        # Get base path
        dir_data = str(pathlib.Path(__file__).parents[2])

        # Predefine for convenience
        self.data_programs: dict = dict()
        self.data_patterns: dict = dict()

        # Get data
        for name, path in [self._programs, self._patterns]:
            full_path = os.path.join(dir_data, "data", path)
            setattr(self, 'data_' + name, self._load_yaml(full_path))

    @property
    @abstractmethod
    def active_window_name(self) -> str:
        """ Return the name of the active window.  """
        pass

    @property
    @abstractmethod
    def retrieve_job(self) -> Job:
        """ Get the current active job.  """
        pass

    @staticmethod
    def _load_yaml(path):
        """ Open a yaml file and return the data.  """
        with open(path) as file:
            data = yaml.safe_load(file)
        return data

    def _retrieve_program(self, program_name, window_name):
        """ Get the specific taks and program from a program name.  """
        for task, programs in self.data_programs.items():
            if programs.get(program_name, None) is not None:
                return task, programs[program_name], window_name
        return (None,) * 3

    def _retrieve_pattern(self, window_name):
        """ Get the specific taks and program by means of pattern matching.  """
        for task, patterns in self.data_patterns.items():
            for pattern, program in patterns.items():
                if len(re.findall(pattern, window_name)) > 0:
                    return task, program, window_name
        return (None,) * 3

