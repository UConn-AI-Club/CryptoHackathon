from typing import Any, List
from dataclasses import dataclass
from dacite import from_dict
from datetime import datetime

from pprint import pprint

@dataclass
class contextClass:
    previous: List

def maxPool(row: List[List[str]], context: dict[str, Any]):
    """
    max pool approach to trading bot

    :param row: the rpcoessed row to be ran
    :param context: persistent context from previous iterations
    """

    response = None

    if not "previous" in context:
        context["previous"] = []

    context = from_dict(data_class=contextClass, data=context)

    print(row)
    context.previous = row

    return context.__dict__
