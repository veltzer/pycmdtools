from typing import List

import click
from pylogconf import setup


@click.command()
@click.option(
    '--from_line',
    required=False,
    default=None,
    type=str,
    help="from what value?",
    show_default=True,
)
@click.option(
    '--to_line',
    required=True,
    default=None,
    type=str,
    help="to what value?",
    show_default=True,
)
@click.argument(
    'filenames',
    required=True,
    nargs=-1,
)
def main(
        from_line: str,
        to_line: str,
        filenames: List[str],
) -> None:
    setup()
    """
    Validate json files
    :param filenames: filenames to change the first line of
    :return: nothing
    """
    for filename in filenames:
        with open(filename, "rt") as input_handle:
            data = input_handle.readlines()
        # change the first line
        if from_line is None or data[0] == from_line+"\n":
            data[0] = to_line+"\n"
        with open(filename, "wt") as output_handle:
            output_handle.write("".join(data))


if __name__ == '__main__':
    main()

