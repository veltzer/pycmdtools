"""
The default group of operations that pycmdtools has
"""
from collections import defaultdict

from pytconf.config import register_endpoint, register_function_group, get_free_args

import pycmdtools
import pycmdtools.version
from pycmdtools.configs import ConfigFolder, ConfigUseStandardExceptions, ConfigChangeLine
from pycmdtools.utils import yield_bad_symlinks, diamond_lines

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pycmdtools commands"


def register_group_default() -> None:
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pycmdtools.version.VERSION_STR)


def error(args):
    raise args


@register_endpoint(
    configs=[
        ConfigFolder,
        ConfigUseStandardExceptions
    ],
)
def find_bad_symlinks() -> None:
    """
    Find all bad symbolic links in a folder
    """
    for full in yield_bad_symlinks(
        folder=ConfigFolder.folder,
        use_standard_exceptions=ConfigUseStandardExceptions.use_standard_exceptions,
        onerror=error,
    ):
        print(full)


@register_endpoint(
    configs=[
        ConfigChangeLine,
    ],
    allow_free_args=True,
)
def change_first_line() -> None:
    """
    Change the first line in files.
    """
    changed = 0
    actually_changed = 0
    print("from_line is [{}]".format(ConfigChangeLine.from_line))
    print("to_line is [{}]".format(ConfigChangeLine.to_line))
    for filename in get_free_args():
        print("considering [{}]...".format(filename))
        with open(filename, "rt") as input_handle:
            data = input_handle.readlines()
        if len(data) == 0:
            continue
        # change the first line
        if ConfigChangeLine.from_line is None or data[0] == ConfigChangeLine.from_line+"\n":
            if data[0] != ConfigChangeLine.to_line+"\n":
                actually_changed += 1
            data[0] = ConfigChangeLine.to_line+"\n"
            changed += 1
        with open(filename, "wt") as output_handle:
            output_handle.write("".join(data))
    # print statistics
    print("changed is [{}]".format(changed))
    print("actually_changed is [{}]".format(actually_changed))


@register_endpoint(
    allow_free_args=True,
)
def line_value_histogram() -> None:
    """
    Print unique values and their count
    """
    saw = defaultdict(int)
    for line in diamond_lines(get_free_args()):
        line = line.rstrip()
        saw[line] += 1
    for k, v in saw.items():
        print('\t'.join([k, str(v)]))


@register_endpoint(
    allow_free_args=True,
)
def unique() -> None:
    """
    Filter out non unique values from a stream, even if not sorted
    """
    saw = set()
    for line in diamond_lines(get_free_args()):
        if line not in saw:
            saw.add(line)
            print(line, end='')
