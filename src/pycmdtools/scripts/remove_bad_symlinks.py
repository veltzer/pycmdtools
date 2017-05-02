import click
from pycmdtools.utils import remove_bad_symlinks


def error(args):
    raise args


@click.command()
def main():
    folder = "."
    use_standard_exceptions = True
    remove_bad_symlinks(folder=folder, use_standard_exceptions=use_standard_exceptions, onerror=error)


if __name__ == '__main__':
    main()
