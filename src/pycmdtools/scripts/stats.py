from typing import List

import click
from pylogconf import setup

from pycmdtools.utils import diamond_lines


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
    stats on standard input
    :param args: 
    :return: 
    """
    total_sum = 0.0
    total_sum2 = 0.0
    count = 0
    for line in diamond_lines(args):
        count += 1
        value = float(line)
        total_sum += value
        total_sum2 += value*value
    print(total_sum/count)

if __name__ == '__main__':
    main()

