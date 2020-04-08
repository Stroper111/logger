from abc import ABC, abstractmethod


class AbstractTracker(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @property
    @abstractmethod
    def active_window_name(self) -> str:
        """ Return the name of the active window.  """
        pass



