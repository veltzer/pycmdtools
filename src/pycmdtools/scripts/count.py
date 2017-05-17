import sys
from collections import defaultdict
from typing import List

import click


def diamond_lines(args: List[str]):
    if not args:
        for line in sys.stdin.readlines():
            yield line
    else:
        for filename in args:
            with open(filename, 'rt') as file_handle:
                for line in file_handle:
                    yield line


@click.command()
@click.argument(
    'args',
    required=False,
    nargs=-1,
)
def main(args: List[str]) -> None:
    """
    Filter out non unique values from a stream, even if not sorted
    :param args: 
    :return: 
    """
    saw = defaultdict(int)
    for line in diamond_lines(args):
        line = line.rstrip()
        saw[line] += 1
    for k, v in saw.items():
        print('\t'.join([k, str(v)]))


if __name__ == '__main__':
    main()

