import boto3
from s3_helper import CSVStream
from datetime import datetime

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
