import argparse
from manager.load_config import CONFIG

def readArguments():
    """
    Read all command line arguments
    """

    parser = argparse.ArgumentParser(description="Arguments to execute different parts of code")
    parser.add_argument(
        "--visualize_tendencies",
        required=False,
        action="store_true",
        help="Generate the class report"
    )
    parser.add_argument(
        "--csv_type",
        required=True,
        type=str,
        help="the csv against which to run"
    )
    parser.add_argument(
        "--set_delimiter",
        required=False,
        type=int,
        help="set a delimiter on the number of rows to run against on data"
    )
    parser.add_argument(
        "--set_offset",
        required=False,
        type=int,
        help="set the offset on the number of rows to skip at beginning of data"
    )
    parser.add_argument(
        "--realtime_run",
        required=False,
        action="store_true",
        help="run realtime test on data"
    )
    parser.add_argument(
        "--load_data",
        required=False,
        action="store_true",
        help="load data to run"
    )

    args = parser.parse_args()

    if not args.csv_type in CONFIG["CSV_OBJ_KEYS"]:
        raise Exception("Specified csv type is not supported")

    if not args.set_offset:
        args.set_offset = 0

    return args
