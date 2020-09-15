"""
The default group of operations that pycmdtools has
"""
import collections
import json
import shutil
from collections import defaultdict

import yaml
from pytconf import register_endpoint, register_function_group, get_free_args
from tqdm import tqdm

import pycmdtools
import pycmdtools.version
from pycmdtools.configs import ConfigFolder, ConfigUseStandardExceptions, ConfigChangeLine, ConfigProgress, \
    ConfigAlgorithm, ConfigDownloadGoogleDrive, ConfigCopy, ConfigDownloadGdriveURL
from pycmdtools.utils import yield_bad_symlinks, diamond_lines, checksum, download_file_from_google_drive, error, \
    remove_bad_symlinks, gdrive_download_link

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
        ConfigFolder,
        ConfigUseStandardExceptions
    ],
)
def symlinks_remove_bad() -> None:
    """
    remove all bad symlinks
    """
    remove_bad_symlinks(
        folder=ConfigFolder.folder,
        use_standard_exceptions=ConfigUseStandardExceptions.use_standard_exceptions,
    )


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


@register_endpoint(allow_free_args=True)
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


@register_endpoint(allow_free_args=True)
def unique() -> None:
    """
    Filter out non unique values from a stream, even if not sorted
    """
    saw = set()
    for line in diamond_lines(get_free_args()):
        if line not in saw:
            saw.add(line)
            print(line, end='')


@register_endpoint(allow_free_args=True)
def print_all_args() -> None:
    """
    print all command line arguments.
    """
    print("number of command line arguments is {}".format(len(get_free_args())))
    for i, s in enumerate(get_free_args()):
        print("{}: {}".format(i, s))


"""
enable to show progress by pointing to a FILE and not a PROCESS NAME or PID.
If you point to a file then something like fuser(1) should be called
on the file, and if there is just one process holding the file open
then show the progress on that file.

References:
- https://unix.stackexchange.com/questions/66795/how-to-check-progress-of-running-cp
- https://github.com/Xfennec/progress
- https://gist.github.com/azat/2830255
- https://stackoverflow.com/questions/10980689/how-to-follow-the-progress-of-a-linux-command
"""


@register_endpoint()
def progress() -> None:
    """
    follow the progress of another process
    """
    pass


@register_endpoint(allow_free_args=True)
def stats() -> None:
    """
    Print statistics about a list of numbers.
    """
    total_sum = 0.0
    total_sum2 = 0.0
    count = 0
    for line in diamond_lines(get_free_args()):
        count += 1
        value = float(line)
        total_sum += value
        total_sum2 += value * value
    if count != 0:
        print(total_sum / count)
    else:
        print("no data given")


@register_endpoint(allow_free_args=True)
def validate_json() -> None:
    """
    Validate json files
    """
    for filename in get_free_args():
        with open(filename, "rt") as input_handle:
            json.load(input_handle)


@register_endpoint(allow_free_args=True)
def validate_yaml() -> None:
    """
    Validate YAML files
    """
    for filename in get_free_args():
        with open(filename, "rt") as input_handle:
            yaml.load(input_handle)


@register_endpoint()
def xprofile_select() -> None:
    """
    Select an x profile with some interface from ~/.xprofilerc
    """
    pass


@register_endpoint(
    configs=[
        ConfigProgress,
        ConfigAlgorithm,
        ConfigCopy,
    ],
    allow_free_args=True,
    min_free_args=2,
)
def mcmp() -> None:
    """
    compare many files and print identical ones
    TODO:
    - make the algorithm faster by looking only at the beginning of the files.
    - make the algorithm faster by looking at the length of the files.
    - make the algorithm faster by having a gnu dbm ~/.mcmp which already stores
    hashes of known files.
    """
    d = collections.defaultdict(set)
    files = get_free_args()
    if ConfigProgress.progress:
        files = tqdm(files)
    for file_name in files:
        check_sum = checksum(file_name=file_name, algorithm=ConfigAlgorithm.algorithm)
        d[check_sum].add(file_name)
    for i, check_sum in enumerate(sorted(d.keys())):
        print("{}: {}".format(i, ", ".join(sorted(d[check_sum]))))
    if ConfigCopy.copy:
        sorted_keys = sorted(d.keys())
        index_from = int(input("From what version? "))
        index_to = int(input("To what version? "))
        checksum_from = sorted_keys[index_from]
        checksum_to = sorted_keys[index_to]
        set_from = d[checksum_from]
        set_to = d[checksum_to]
        source_file = set_from.pop()
        for target_file in set_to:
            shutil.copy(source_file, target_file)


@register_endpoint(configs=[
    ConfigDownloadGoogleDrive,
])
def google_drive_download_by_id() -> None:
    """
    Download a file from a google drive using it's id.

    If you have a link to a google drive file like this:
    https://drive.google.com/open?id=0BwNoUKizWBdnRmRmLVlWSWxzWnM
    or like this:
    https://drive.google.com/file/d/0BwNoUKizWBdnSHF4SFlyRkxNSVE/view?usp=sharing
    Then the file id of the relevant files are:
    0BwNoUKizWBdnRmRmLVlWSWxzWnM
    0BwNoUKizWBdnSHF4SFlyRkxNSVE
    And this is what you have to supply to this script to download the files.

    References:
    - http://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive
    """
    download_file_from_google_drive(
        ConfigDownloadGoogleDrive.file_id,
        ConfigDownloadGoogleDrive.destination,
    )


@register_endpoint(configs=[
    ConfigDownloadGdriveURL,
])
def google_drive_download_by_url() -> None:
    """
    Download a file shared from a google drive using a link
    :return:
    """
    gdrive_download_link(url=ConfigDownloadGdriveURL.url)
