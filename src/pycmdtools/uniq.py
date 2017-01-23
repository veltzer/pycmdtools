import sys


def diamond_lines():
    if len(sys.argv) == 1:
        for line in sys.stdin.readlines():
            yield line
    else:
        for filename in sys.argv[1:]:
            with open(filename, 'rt') as file_handle:
                for line in file_handle:
                    yield line


def main():
    saw = set()
    for line in diamond_lines():
        if line not in saw:
            saw.add(line)
            print(line, end='')


if __name__ == '__main__':
    main()

