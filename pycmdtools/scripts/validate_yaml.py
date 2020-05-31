import yaml
from typing import List

import click


@click.command()
@click.argument(
    'args',
    required=True,
    nargs=-1,
)
def validate_yaml(
        args: List[str],
) -> None:
    """
    Validate YAML files
    :param args: files to validate
    :return: nothing
    """
    for filename in args:
        with open(filename, "rt") as input_handle:
            yaml.load(input_handle)
