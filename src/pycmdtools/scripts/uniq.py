import sys
import click


def diamond_lines(args):
    if not args:
        for line in sys.stdin.readlines():
            yield line
    else:
        for filename in args:
            with open(filename, 'rt') as file_handle:
                for line in file_handle:
                    yield line


@click.command()
@click.argument('args', nargs=-1)
def main(args):
    saw = set()
    for line in diamond_lines(args):
        if line not in saw:
            saw.add(line)
            print(line, end='')


if __name__ == '__main__':
    main()

