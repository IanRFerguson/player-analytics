import argparse


def cli():
    """
    Handles command line arguments when executing `run.py`

    ```
    # Run workflow outside of Prefect context
    python3 src/run.py --local

    # Activate debugging
    python3 src/run.py --debug

    # Debugging, local run, full refresh, you get it
    python3 src/run.py -l -f -d
    ```
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--full-refresh", "-f", action="store_true", default=False)
    parser.add_argument("--debug", "-d", action="store_true", default=False)
    parser.add_argument("--test", "-t", action="store_true", default=False)
    parser.add_argument("--local", "-l", action="store_true", default=False)

    return parser.parse_args()
