from maxPool.maxPool import maxPool

@dataclass
class Trade:
    trade_type: str # BUY | SELL
    base: str
    volume: Decimal

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
        yield None

    print(f"Succesfully parsed ROW: '{row}'")

    yield Trade(
        trade_type="",
        base="",
        volume=""
    )
