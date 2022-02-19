from manager.args import readArguments

# from process.loadData import loadData, loadDataRealtime
from visualize.visualizeTendency import visualizeTendency

from decimal import Decimal
from typing import Any
from maxPool.maxPool import maxPool
from process.models import Trade

from datetime import datetime

def algorithm(csv_row: str, context: dict[str, Any],):
    """ Trading Algorithm

    Add your logic to this function. This function will simulate a streaming
    interface with exchange trade data. This function will be called for each
    data row received from the stream.

    The context object will persist between iterations of your algorithm.

    Args:
        csv_row (str): one exchange trade (format: "exchange pair", "price", "volume", "timestamp")
        context (dict[str, Any]): a context that will survive each iteration of the algorithm

    Generator:
        response (dict): "Fill"-type object with information for the current and unfilled trades

    Yield (None | Trade | [Trade]): a trade order/s; None indicates no trade action
    """

    row = []
    print()
    try:
        row = csv_row.split(",")
        exchange = row[0]
        price = float(row[1])
        amount = float(row[2])
        timestamp = datetime.fromtimestamp(float(row[3]))

        if timestamp < datetime(2009, 2, 3):
            raise Exception("Timestamp error before creation of crypto")
    except Exception as e:
        print(f"Error parsing row, skipping... ROW: '{csv_row}'")
        yield None
        return

    print(f"Succesfully parsed ROW: '{csv_row}'")

    yield from maxPool([exchange, price, amount, timestamp], context)
    return

import boto3
from s3_helper import CSVStream

# include local modules
from manager.load_config import CONFIG # load configuration file from local yaml

def loadData(csv_type: str, delimiter: int=None, offset: int=0):
    """
    Load the data from the s3

    :param csv_type: the specific csv to load from the s3 bucket
    :param delimiter: the max number of rows to pull from
    """

    # setup the aws session, open s3 and start piping it into csv  stream
    session = boto3.Session(
        aws_access_key_id=CONFIG["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=CONFIG["AWS_SECRET_ACCESS_KEY"]
    )
    s3 = session.resource("s3")
    bucket = s3.Bucket(CONFIG["BUCKET_NAME"])

    SELECT_ALL_QUERY = "SELECT * from S3Object"

    STREAM = CSVStream(
        "select",
        session,
        key=CONFIG["CSV_OBJ_KEYS"][csv_type],
        bucket=CONFIG["BUCKET_NAME"],
        expression=SELECT_ALL_QUERY
    )

    # Iterate over the rows in the stream and save to data
    data = []
    cnt_offset = 0
    cnt_delimiter = 0
    for row in STREAM.iter_records():
        if cnt_offset <= offset:
            cnt_offset += 1
            continue

        try:
            row = row.split(",")
            exchange = row[0]
            price = float(row[1])
            amount = float(row[2])
            timestamp = datetime.fromtimestamp(float(row[3]))
            if timestamp < datetime(2009, 2, 3):
                raise Exception("Timestamp error before creation of crypto")
        except Exception as e:
            print(f"Error parsing row, skipping... ROW: '{row}'")
            continue

        data.append([exchange, price, amount, timestamp])
        print(f"Succesfully parsed ROW: '{row}'")

        if delimiter is not None:
            cnt_delimiter += 1
            if cnt_delimiter == delimiter:
                break

    return data

def loadDataRealtime(csv_type: str, delimiter: int=None, offset: int=0):
    """
    Load data and pass through algorith in realtime

    :param csv_type: the specific csv to load from the s3 bucket
    :param delimiter: the max number of rows to pull from
    """

    # setup the aws session, open s3 and start piping it into csv  stream
    session = boto3.Session(
        aws_access_key_id=CONFIG["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=CONFIG["AWS_SECRET_ACCESS_KEY"]
    )
    s3 = session.resource("s3")
    bucket = s3.Bucket(CONFIG["BUCKET_NAME"])

    SELECT_ALL_QUERY = "SELECT * from S3Object"

    STREAM = CSVStream(
        "select",
        session,
        key=CONFIG["CSV_OBJ_KEYS"][csv_type],
        bucket=CONFIG["BUCKET_NAME"],
        expression=SELECT_ALL_QUERY
    )

    # setting up algorithm context
    context = {}

    # Iterate over the rows in the stream and save to data
    cnt_offset = 0
    cnt_delimiter = 0
    for row in STREAM.iter_records():
        if cnt_offset <= offset:
            cnt_offset += 1
            continue

        for trade in algorithm(row, context):
            print(trade)

        if delimiter is not None:
            cnt_delimiter += 1
            if cnt_delimiter == delimiter:
                break

    return


def main():
    args = readArguments()

    data = []
    if args.load_data:
        data = loadData(args.csv_type, delimiter=args.set_delimiter, offset=args.set_offset)

    if args.visualize_tendencies:
        visualizeTendency(data)

    if args.realtime_run:
        loadDataRealtime(args.csv_type, delimiter=args.set_delimiter, offset=args.set_offset)

# Run if run as script
if __name__ == '__main__':
    main()
