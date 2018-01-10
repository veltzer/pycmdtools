import click
from pylogconf.core import setup
from typing import List


@click.command()
@click.argument(
    'args',
    required=False,
    nargs=-1,
)
def main(
    args: List[str],
) -> None:
    """
        print all command line arguments in an explicit way.
        This can be used for testing command line programs.
        :return:
    """
    setup()
    print("number of command line arguments is {}".format(len(args)))
    for i, s in enumerate(args):
        print("{}: {}".format(i, s))


if __name__ == '__main__':
    main()
