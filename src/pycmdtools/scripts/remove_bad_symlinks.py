import click
from pycmdtools.utils import remove_bad_symlinks


def error(args):
    raise args


@click.command()
@click.option(
    '--folder',
    required=False,
    default=".",
    type=str,
    help="which folder to scan"
)
@click.option(
    '--use_standard_exceptions',
    required=False,
    default=True,
    type=bool,
    help="skip standard symbolic links like browser lock files"
)
def main(folder: str, use_standard_exceptions: bool) -> None:
    """
    remove bad symbolic links from a folder
    :return: 
    """
    remove_bad_symlinks(folder=folder, use_standard_exceptions=use_standard_exceptions, onerror=error)


if __name__ == '__main__':
    main()
