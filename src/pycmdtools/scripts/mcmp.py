"""
This script compares many files
"""
import collections
import hashlib
import functools
import click


def checksum(file_name: str=None, algorithm: str=None) -> str:
    """
    calculate a checksum of a file. You dictate which algorithm.
    If you want to see all algorithms try:
    hashlib.algorithms_available
    :param file_name:
    :param algorithm:
    :return:
    """
    block_size = 65536
    with open(file_name, mode='rb') as f:
        hash_object = hashlib.new(algorithm)
        for buf in iter(functools.partial(f.read, block_size), b''):
            hash_object.update(buf)
    return hash_object.hexdigest()


@click.command()
@click.option('--algorithm', required=False, default='md5',
              type=click.Choice(hashlib.algorithms_available), help="algorithm to use")
@click.argument('files', required=True, type=str, nargs=-1)
def main(algorithm, files):
    d = collections.defaultdict(set)
    for file_name in files:
        check_sum = checksum(file_name=file_name, algorithm=algorithm)
        d[check_sum].add(file_name)
    for i, check_sum in enumerate(sorted(d.keys())):
        print("{}: {}".format(i, ", ".join(sorted(d[check_sum]))))


if __name__ == '__main__':
    main()
