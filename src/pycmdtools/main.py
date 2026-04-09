"""
The default group of operations that pycmdtools has
"""
import collections
import json
import os
import sys
import shutil
from collections import defaultdict
from typing import DefaultDict
import csv

import pylogconf.core
import yaml
import jsonschema
from ruamel.yaml import YAML
from jsonschema import Draft7Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT7
from pytconf import register_endpoint, get_free_args, register_main, config_arg_parse_and_launch
from tqdm import tqdm
from lxml import etree
import html5lib

from pycmdtools.configs import ConfigFolder, ConfigUseStandardExceptions, ConfigChangeLine, ConfigProgress, \
    ConfigAlgorithm, ConfigDownloadGoogleDrive, ConfigCopy, ConfigDownloadGdriveURL, ConfigOutput, ConfigDebug, \
    ConfigUseCache, ConfigSchemaUrl
from pycmdtools import schema_cache
from pycmdtools.static import DESCRIPTION, APP_NAME, VERSION_STR
from pycmdtools.utils import yield_bad_symlinks, diamond_lines, checksum, download_file_from_google_drive, error, \
    remove_bad_symlinks, gdrive_download_link
from pycmdtools.python import do_python_check_syntax


@register_endpoint(
    description="Find all bad symbolic links in a folder",
    configs=[
        ConfigFolder,
        ConfigUseStandardExceptions
    ],
)
def symlinks_find_bad() -> None:
    for full in yield_bad_symlinks(
        folder=ConfigFolder.folder,
        use_standard_exceptions=ConfigUseStandardExceptions.use_standard_exceptions,
        onerror=error,
    ):
        print(full)


@register_endpoint(
    description="remove all bad symlinks",
    configs=[
        ConfigFolder,
        ConfigUseStandardExceptions
    ],
)
def symlinks_remove_bad() -> None:
    remove_bad_symlinks(
        folder=ConfigFolder.folder,
        use_standard_exceptions=ConfigUseStandardExceptions.use_standard_exceptions,
    )


@register_endpoint(
    description="Change the first line in files",
    configs=[
        ConfigChangeLine,
    ],
    allow_free_args=True,
)
def change_first_line() -> None:
    changed = 0
    actually_changed = 0
    print(f"from_line is [{ConfigChangeLine.from_line}]")
    print(f"to_line is [{ConfigChangeLine.to_line}]")
    for filename in get_free_args():
        print(f"considering [{filename}]...")
        with open(filename) as input_handle:
            data = input_handle.readlines()
        if len(data) == 0:
            continue
        # change the first line
        if ConfigChangeLine.from_line is None or data[0] == ConfigChangeLine.from_line + "\n":
            if data[0] != ConfigChangeLine.to_line + "\n":
                actually_changed += 1
            data[0] = ConfigChangeLine.to_line + "\n"
            changed += 1
        with open(filename, "w") as output_handle:
            output_handle.write("".join(data))
    # print statistics
    print(f"changed is [{changed}]")
    print(f"actually_changed is [{actually_changed}]")


@register_endpoint(
    description="Print unique values and their count",
    allow_free_args=True
)
def line_value_histogram() -> None:
    saw: DefaultDict[str, int] = defaultdict(int)
    for line in diamond_lines(get_free_args()):
        line = line.rstrip()
        saw[line] += 1
    for k, v in saw.items():
        print(f"{k}\t{str(v)}")


@register_endpoint(
    description="Filter out non unique values from a stream, even if not sorted",
    allow_free_args=True
)
def unique() -> None:
    saw = set()
    for line in diamond_lines(get_free_args()):
        if line not in saw:
            saw.add(line)
            print(line, end="")


@register_endpoint(
    description="check python files for syntax",
    allow_free_args=True
)
def python_check_syntax() -> None:
    for filename in get_free_args():
        do_python_check_syntax(filename)


@register_endpoint(
    description="print all command line arguments",
    allow_free_args=True
)
def print_all_args() -> None:
    print(f"number of command line arguments is {len(get_free_args())}")
    for i, s in enumerate(get_free_args()):
        print(f"{i}: {s}")


@register_endpoint(
    description="follow the progress of another process",
)
def progress() -> None:
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


@register_endpoint(
    description="Print statistics about a list of numbers",
    allow_free_args=True
)
def stats() -> None:
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


@register_endpoint(
    description="Validate json files",
    allow_free_args=True,
)
def validate_json() -> None:
    for filename in get_free_args():
        with open(filename) as input_handle:
            json.load(input_handle)


@register_endpoint(
    description="Validate csv files",
    allow_free_args=True,
)
def validate_csv() -> None:
    for filename in get_free_args():
        with open(filename) as input_handle:
            _ = csv.DictReader(input_handle).fieldnames
            for _i, _row in enumerate(csv.reader(input_handle), 2):
                pass


@register_endpoint(
    description="Count csv lines",
    allow_free_args=True,
)
def linecount_csv() -> None:
    for filename in get_free_args():
        with open(filename) as input_handle:
            _ = csv.DictReader(input_handle).fieldnames
            count = 0
            for _i, _row in enumerate(csv.reader(input_handle), 2):
                count = count + 1
            print(f"[{filename}] line count is [{count}]")


@register_endpoint(
    description="Validate YAML files",
    allow_free_args=True,
    min_free_args=1,
)
def validate_yaml() -> None:
    for filename in get_free_args():
        with open(filename) as input_handle:
            yaml.load(input_handle, yaml.SafeLoader)


def _check_order_recursively(data, schema, filename, path="", debug=False) -> bool:
    is_valid = True
    if debug:
        print(f"DEBUG: Checking order at path [{path}]")
    if isinstance(data, dict):
        if "propertyOrdering" in schema:
            expected_order = schema["propertyOrdering"]
            actual_keys = list(data.keys())
            ordered_actual_keys = [key for key in expected_order if key in actual_keys]
            if ordered_actual_keys != [key for key in actual_keys if key in expected_order]:
                line_num = data.lc.line if hasattr(data, "lc") else "N/A"
                print(f"Error in filename: {filename}:{line_num}")
                print(f"Property Order FAILED at path: {path}")
                print(f"Expected order of keys: {expected_order}")
                print(f"Actual order of keys: {actual_keys}")
                is_valid = False
        for key, value in data.items():
            sub_schema = schema.get("properties", {}).get(key)
            if sub_schema:
                new_path = f"{path}.{key}" if path else key
                if not _check_order_recursively(value, sub_schema, filename, new_path, debug):
                    is_valid = False
    elif isinstance(data, list):
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                if not _check_order_recursively(item, item_schema, filename, new_path, debug):
                    is_valid = False
    return is_valid


@register_endpoint(
    description="Validate YAML files against JSON schema with property order checking",
    configs=[
        ConfigDebug,
        ConfigUseCache,
    ],
    allow_free_args=True,
    min_free_args=1,
)
def validate_yaml_advanced() -> None:
    memory_cache: dict = {}
    use_cache = ConfigUseCache.use_cache
    errors = False
    for yaml_file in get_free_args():
        ruamel = YAML(typ="rt")
        with open(yaml_file, encoding="UTF8") as f:
            data = ruamel.load(f)
        schema_url = data.get("$schema")
        if not schema_url:
            print(f"Error: [{yaml_file}] does not contain a $schema URL reference")
            sys.exit(1)
        fetched = schema_cache.fetch_schema(schema_url, use_cache, memory_cache)

        def retriever(uri):
            return Resource.from_contents(schema_cache.fetch_schema(uri, use_cache, memory_cache))

        resource = Resource.from_contents(fetched, default_specification=DRAFT7)
        registry = Registry(retrieve=retriever).with_resource(schema_url, resource)  # type: ignore[call-arg]
        validator = Draft7Validator(fetched, registry=registry)
        validator.validate(data)

        if not _check_order_recursively(data, fetched, yaml_file, debug=ConfigDebug.debug):
            errors = True
    if errors:
        sys.exit(1)


@register_endpoint(
    description="List all cached schemas",
)
def schema_cache_list() -> None:
    entries = schema_cache.list_entries()
    if not entries:
        print("Schema cache is empty")
        return
    for url, path in entries:
        print(f"{url}\n  {path}")
    print(f"\n{len(entries)} cached schema(s)")


@register_endpoint(
    description="Clear all cached schemas",
)
def schema_cache_clear() -> None:
    count = schema_cache.clear_all()
    print(f"Removed {count} cached schema(s)")


@register_endpoint(
    description="Remove a specific schema from the cache by URL",
    configs=[
        ConfigSchemaUrl,
    ],
)
def schema_cache_remove() -> None:
    if schema_cache.remove_entry(ConfigSchemaUrl.schema_url):
        print(f"Removed cached schema for {ConfigSchemaUrl.schema_url}")
    else:
        print(f"No cached schema found for {ConfigSchemaUrl.schema_url}")


@register_endpoint(
    description="Validate jsonschame files",
    allow_free_args=True,
    min_free_args=1,
)
def validate_jsonschema() -> None:
    for filename in get_free_args():
        with open(filename) as stream:
            data = json.load(stream)
            validator = jsonschema.validators.validator_for(data)
            validator.check_schema(data)


@register_endpoint(
    description="Validate XML files",
    allow_free_args=True
)
def validate_xml() -> None:
    for filename in get_free_args():
        etree.parse(filename)


@register_endpoint(
    description="Pick an x profile with some interface from ~/.xprofilerc",
)
def xprofile_select() -> None:
    print("TBD")


@register_endpoint(
    description="compare many files and print identical ones",
    configs=[
        ConfigProgress,
        ConfigAlgorithm,
        ConfigCopy,
        ConfigOutput,
    ],
    allow_free_args=True,
    min_free_args=2,
)
def mcmp() -> None:
    """
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
    if ConfigOutput.print is None:
        for i, check_sum in enumerate(sorted(d.keys())):
            formatted = ", ".join(sorted(d[check_sum]))
            print(f"{i}: {formatted}")
    else:
        if len(d.keys()) > 1:
            print(ConfigOutput.print)
    if ConfigCopy.copy:
        if len(d.keys()) > 1:
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
        else:
            print("All copies are identical, cannot copy")


@register_endpoint(
    description="Download a file from a google drive using its id",
    configs=[ConfigDownloadGoogleDrive],
)
def google_drive_download_by_id() -> None:
    """
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


@register_endpoint(
    description="Download a file shared from a google drive using a link",
    configs=[ConfigDownloadGdriveURL],
)
def google_drive_download_by_url() -> None:
    gdrive_download_link(url=ConfigDownloadGdriveURL.url)


@register_endpoint(
    description="Extension stats",
    allow_free_args=True,
)
def extension_stats():
    counter = collections.Counter()
    for filename in get_free_args():
        _, extension = os.path.splitext(filename)
        if len(extension) >= 1 and extension[0] == ".":
            extension = extension[1:]
        counter.update([extension])
    # pretty print the counter object
    total = 0
    # most common returns all elements if not passed a value,
    # sorted in value order with highest first
    for value, count in counter.most_common():
        print(f"{value} {count}")
        total += count
    print(f"total is {total}")


@register_endpoint(
    description="Validate HTML files",
    allow_free_args=True,
    min_free_args=1,
)
def validate_html():
    errors = []
    for filename in get_free_args():
        with open(filename, encoding="utf-8") as stream:
            parser = html5lib.HTMLParser(strict=True)

            def error_handler(message):
                print(message, file=sys.stderr)
                errors.append(message)
            parser.errors = error_handler
            try:
                parser.parse(stream)
            except html5lib.html5parser.ParseError as e:
                value = str(e)
                print(value)
                errors.append(value)
    sys.exit(len(errors) > 0)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
