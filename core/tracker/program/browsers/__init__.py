

import platform

if platform.system() == "Windows":
    from .windows import Firefox
    from .windows import Chrome
    from .windows import Tor

if platform.system() == "Linux":
    raise NotImplementedError

if platform.system() == "Java":
    raise NotImplementedError