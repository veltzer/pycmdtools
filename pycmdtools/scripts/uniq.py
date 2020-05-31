from typing import List

import click

from pycmdtools.utils import diamond_lines


@click.command()
@click.argument(
    'args',
    required=False,
    nargs=-1,
)
def uniq(
        args: List[str],
) -> None:
    """
    Filter out non unique values from a stream, even if not sorted
    :param args: 
    :return: 
    """
    saw = set()
    for line in diamond_lines(args):
        if line not in saw:
            saw.add(line)
            print(line, end='')
