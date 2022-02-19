from typing import Any, List
from dataclasses import dataclass
from dacite import from_dict
from datetime import datetime

from pprint import pprint

@dataclass
class contextClass:
    previous: List


def maxPool(row: str, context: dict[str, Any]):
    """
    max pool approach to trading bot

    :param row: the row from the csv file to be processed
    :param context: persistent context from previous iterations
    """

    # try parsing current row
    try:
        row = row.split(",")
        exc = row[0]
        price = float(row[1])
        amount = float(row[2])
        time = datetime.fromtimestamp(int(row[3]))
    except:
        print(f"shit happened row: {row}")
        return context

    response = None

    if not "previous" in context:
        context["previous"] = []

    context = from_dict(data_class=contextClass, data=context)

    print(row)
    context.previous = row

    return context.__dict__
