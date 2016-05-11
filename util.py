import sys


def print_line(w):
    sys.stdout.write(w)
    sys.stdout.flush()


class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

