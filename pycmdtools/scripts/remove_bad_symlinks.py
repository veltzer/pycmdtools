import os

import click
from pylogconf import setup

from pycmdtools.utils import yield_bad_symlinks


def error(args):
    raise args


@click.command()
@click.option(
    '--folder',
    required=False,
    default=".",
    type=str,
    help="which folder to scan",
    show_default=True,
)
@click.option(
    '--use_standard_exceptions',
    required=False,
    default=True,
    type=bool,
    help="skip standard symbolic links like browser lock files",
    show_default=True,
)
def main(
        folder: str,
        use_standard_exceptions: bool,
) -> None:
    setup()
    """
    remove bad symbolic links from a folder
    :return: 
    """
    for full in yield_bad_symlinks(
            folder=folder,
            use_standard_exceptions=use_standard_exceptions,
            onerror=error,
    ):
        print("removing [{}]".format(full))
        os.unlink(full)


if __name__ == '__main__':
    main()