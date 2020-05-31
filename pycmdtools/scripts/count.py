from collections import defaultdict
from typing import List

import click

from pycmdtools.utils import diamond_lines


@click.command()
@click.argument(
    'args',
    required=False,
    nargs=-1,
)
def count(
        args: List[str],
) -> None:
    """
    print unique values and their count
    :param args:
    :return: 
    """
    saw = defaultdict(int)
    for line in diamond_lines(args):
        line = line.rstrip()
        saw[line] += 1
    for k, v in saw.items():
        print('\t'.join([k, str(v)]))
