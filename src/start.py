import argparse
import os


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        dest="config",
        required=True,
        help="config file",
        metavar="FILE",
        type=lambda x: is_valid_file(parser, x),
    )
    args = parser.parse_args()
