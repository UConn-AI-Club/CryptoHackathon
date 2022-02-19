from typing import Any, List
from dataclasses import dataclass
from dacite import from_dict
from datetime import datetime

from pprint import pprint

from process.models import Trade

@dataclass
class contextClass:
    prev_row: List
    load_sum: float
    load_cnt: float
    prev_load_avg: float
    cur_crypto: float
    trend_cnt: float

def maxPool(row: List[Any], context: dict[str, Any]):
    """
    max pool approach to trading bot

    :param row: the rpcoessed row to be ran
    :param context: persistent context from previous iterations
    """

    if "xbt" not in context:
        context["xbt"] = {}
    if "eth" not in context:
        context["eth"] = {}
    if "usd" not in context:
        context["usd"] = 1000000.00


    print("USD HOLDING:", context["usd"])
    if "cur_crypto" in context["xbt"]:
        print("XBT HOLDING:", context["xbt"]["cur_crypto"])
    if "cur_crypto" in context["eth"]:
        print("ETH MHOLDING:", context["eth"]["cur_crypto"])

    yield from __cryptoMaxPool(row, context, "xbt" if "xbt" in row[0] else "eth")
    return

def __cryptoMaxPool(row: List[Any], context: dict[str, Any], crypto_type: str):

    c_context = context[crypto_type]

    if not "prev_row" in c_context:
        c_context["prev_row"] = row
        c_context["load_sum"] = row[1]
        c_context["load_cnt"] = 1
        c_context["prev_load_avg"] = -1
        c_context["cur_crypto"] = 0
        c_context["trend_cnt"] = 1
        context[crypto_type] = c_context
        yield None
        return

    c_context = from_dict(data_class=contextClass, data=c_context)

    if c_context.prev_row[3] == row[3]:
        print("CALCULATING LOAD AVG")
        c_context.load_sum += row[1]
        c_context.load_cnt += 1
        context[crypto_type] = c_context.__dict__.copy()
        yield None
        return

    load_avg =c_context.load_sum /c_context.load_cnt
    c_context.prev_row = row
    c_context.load_sum = row[1]
    c_context.load_cnt = 1

    if c_context.prev_load_avg == -1:
        c_context.prev_load_avg = load_avg
        context[crypto_type] = c_context.__dict__.copy()
        yield None
        return

    if c_context.prev_load_avg < row[1]:
        invest_amount = row[1]/((context["usd"]/c_context.trend_cnt)*0.6)
        print("BUYING")

        yield Trade(
            trade_type="BUY",
            base=crypto_type,
            volume=invest_amount
        )

        c_context.trend_cnt += c_context.trend_cnt/1.5
        c_context.cur_crypto += invest_amount
        context["usd"] -= ((context["usd"]/c_context.trend_cnt)*0.6)
    else:
        print("SELLING IF HAVE")
        yield Trade(
            trade_type="SELL",
            base=crypto_type,
            volume=c_context.cur_crypto
        )

        context["usd"] += c_context.cur_crypto * row[1]
        c_context.cur_crypto = 0
        c_context.trend_cnt = 1

    c_context.prev_load_avg = load_avg
    context[crypto_type] = c_context.__dict__.copy()

    return
