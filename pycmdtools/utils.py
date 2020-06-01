import os
import os.path
import logging

from typing import Callable, List

import sys

# These are symbolic links used for locks in standard users directories
__standard_exceptions__ = {
    'lock',  # firefox lock, $HOME/.mozilla/firefox/[XXX].default/lock
    'SingletonCookie',  # chrome lock, /home/mark/.config/google-chrome/SingletonCookie
    'SingletonLock',  # chrome lock, /home/mark/.config/google-chrome/SingletonLock
    'SingletonSocket',  # chrome lock, /home/mark/.config/google-chrome/SingletonSocket
}


def yield_bad_symlinks(
    folder: str = ".",
    use_standard_exceptions: bool = True,
    onerror: Callable = None,
):
    """
    remove bad symbolic links from a folder.

    Control this functions verbosity using the python logging framework
    :param folder:
    :param use_standard_exceptions:
    :param onerror: passed to os.walk
    :return:
    """
    logger = logging.getLogger(__name__)
    for root, _dirs, files in os.walk(folder, onerror=onerror):
        for file in files:
            if use_standard_exceptions and file in __standard_exceptions__:
                continue
            full = os.path.join(root, file)
            if os.path.islink(full):
                dereference_name = os.readlink(full)
                if not os.path.isabs(dereference_name):
                    dereference_name = os.path.join(root, dereference_name)
                if not os.path.exists(dereference_name):
                    logger.debug("found bad symlink [%s]...", full)
                    yield full


def diamond_lines(filenames: List[str]):
    if not filenames:
        for line in sys.stdin.readlines():
            yield line
    else:
        for filename in filenames:
            with open(filename, 'rt') as file_handle:
                for line in file_handle:
                    yield line
