"""
This script compares many files
"""
import sys
import collections
import hashlib
import functools
import click


def checksum(filename: str=None, algorithm: str=None) -> str:
    """
    calculate a checksum of a file. You dictate which algorithm.
    If you want to see all algorithms try:
    hashlib.algorithms_available
    :param filename:
    :param algorithm:
    :return:
    """
    block_size = 65536
    with open(filename, mode='rb') as f:
        hash_object = hashlib.new(algorithm)
        for buf in iter(functools.partial(f.read, block_size), b''):
            hash_object.update(buf)
    return hash_object.hexdigest()


@click.command()
@click.option('--algorithm', required=False, default='md5',
              type=click.Choice(hashlib.algorithms_available))
def main(algorithm):
    file_names = sys.argv[1:]
    d = collections.defaultdict(set)
    for file_name in file_names:
        check_sum = checksum(file_name=file_name, algorithm=algorithm)
        d[check_sum].add(file_name)
    for check_sum, set_of_files in d.items():
        print(", ".join(set_of_files))


if __name__ == '__main__':
    main()
