import platform

if platform.system() == "Windows":
    from .windows import Tracker

if platform.system() == "Linux":
    raise NotImplementedError

if platform.system() == "Java":
    raise NotImplementedError