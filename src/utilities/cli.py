import argparse

#####


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("--full-refresh", "-f", action="store_true", default=False)
    parser.add_argument("--debug", "-d", action="store_true", default=False)
    parser.add_argument("--test", "-t", action="store_true", default=False)
    parser.add_argument("--local", "-l", action="store_true", default=False)

    return parser.parse_args()
