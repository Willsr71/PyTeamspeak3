import sys
import json


def get_json_file(file_name):
    try:
        return json.loads(open(file_name).read())
    except FileNotFoundError:
        print("File does not exist")
        sys.exit(1)


def set_json_file(file_name, json_arr, indents):
    if indents:
        indents = 2
    else:
        indents = None

    return open(file_name, 'w').write(json.dumps(json_arr, indent=indents))


def print_line(w):
    sys.stdout.write(w)
    sys.stdout.flush()


class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
