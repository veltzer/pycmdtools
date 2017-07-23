import json
from typing import List

import click
from pylogconf import setup


@click.command()
@click.argument(
    'args',
    required=False,
    nargs=-1,
    show_default=True,
)
def main(
        args: List[str],
) -> None:
    setup()
    """
    Validate json files
    :param args: files to validate
    :return: nothing
    """
    for filename in args:
        with open(filename, "rt") as input_handle:
            json.load(input_handle)


if __name__ == '__main__':
    main()

