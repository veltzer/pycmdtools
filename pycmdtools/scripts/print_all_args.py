import sys


def print_all_args() -> None:
    """
        print all command line arguments in an explicit way.
        This can be used for testing command line programs.

        This utility doesn't use click on purpose
        :return:
    """
    print("number of command line arguments is {}".format(len(sys.argv)))
    for i, s in enumerate(sys.argv):
        print("{}: {}".format(i, s))
