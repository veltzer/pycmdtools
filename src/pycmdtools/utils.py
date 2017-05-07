import os
import os.path
import logging

from typing import Callable

"""
These are symbolic links used for locks in standard users directories
"""
standard_exceptions = {
    'lock',  # firefox lock, $HOME/.mozilla/firefox/[XXX].default/lock
    'SingletonCookie',  # chrome lock, /home/mark/.config/google-chrome/SingletonCookie
    'SingletonLock',  # chrome lock, /home/mark/.config/google-chrome/SingletonLock
    'SingletonSocket',  # chrome lock, /home/mark/.config/google-chrome/SingletonSocket
}

logger = logging.getLogger(__name__)


def remove_bad_symlinks(
        folder: str=None,
        use_standard_exceptions: bool=True,
        onerror: Callable=None) -> None:
    """
    remove bad symbolic links from a folder.
    
    Control this functions verbosity using the python logging framework
    :param folder: 
    :param use_standard_exceptions: 
    :param onerror: passed to os.walk
    :return: 
    """
    for root, dirs, files in os.walk(folder, onerror=onerror):
        for file in files:
            if use_standard_exceptions and file in standard_exceptions:
                continue
            full = os.path.join(root, file)
            if os.path.islink(full):
                dereference_name = os.readlink(full)
                if not os.path.isabs(dereference_name):
                    dereference_name = os.path.join(root, dereference_name)
                if not os.path.exists(dereference_name):
                    logger.info("removing bad symlink [%s]...", full)
                    os.unlink(full)
