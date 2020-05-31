import json
from typing import List

import click


@click.command()
@click.argument(
    'args',
    required=True,
    nargs=-1,
)
def validate_json(
        args: List[str],
) -> None:
    """
    Validate json files
    :param args: files to validate
    :return: nothing
    """
    for filename in args:
        with open(filename, "rt") as input_handle:
            json.load(input_handle)
