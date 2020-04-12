import multiprocessing
import win32gui


class TimeOut:
    def __init__(self, limit=0.2):
        """ If there are decorator arguments, the function to be decorated is not passed to the constructor!  """
        self.__timeout = limit
        self.__pool = multiprocessing.Pool(processes=1)

    @property
    def active_window(self):
        return self.__wrapper()

    def __wrapper(self):
        """ Return a wrapper for a the async window catching.  """
        try:
            task = self.__pool.apply_async(self.active_window_name)
            return task.get(timeout=self.__timeout)
        except multiprocessing.context.TimeoutError:
            print("\nTimeoutError")
            return 'Unknown'

    @staticmethod
    def active_window_name() -> str:
        window = win32gui.GetForegroundWindow()
        window_name = win32gui.GetWindowText(window)
        return window_name


if __name__ == '__main__':
    timeout = TimeOut(0.1)
    while True:
        print(timeout.active_window)
