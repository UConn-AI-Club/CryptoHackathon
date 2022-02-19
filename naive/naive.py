import pandas as pd
from process.algorithm import Trade

_store_xbt = pd.DataFrame(columns=["pair", "price", "timestamp"])
_store_eth = pd.DataFrame(columns=[])


def naive(row: List, context: dict):

    if "xbt-usd" in row[0]:

        return _xbt(row)
    else:
        return _eth(row)


def _xbt(row: List):

    if _store_xbt.shape[0] == 0:
        _store_xbt.append(row)
        #  yeild a buy of at given price so we have something in the pot
        yield Trade(trade_type="BUY", base="XBT", volume=2)

    else:
        """
        In the shift you would return the last element, but we need to append that to it first, which makes it the second to last element.
        """
        _store_xbt.append(row)
        if _store_xbt["price"].iloc[-1] > _store_xbt["price"].iloc[-2]:
            #  we have a buy opportunity
            yield Trade(trade_type="BUY", base="XBT", volume=2)
        elif _store_xbt["price"].iloc[-1] < _store_xbt["price"].iloc[-2]:
            #  we have a sell opportunity
            yield Trade(trade_type="SELL", base="XBT", volume=2)


def _eth(row: List):
    if _store_eth.shape[0] == 0:
        _store_eth.append(row)
        #  yeild a buy of at given price so we have something in the pot
        yield Trade(trade_type="BUY", base="ETH", volume=2)

    else:
        """
        In the shift you would return the last element, but we need to append that to it first, which makes it the second to last element.
        """
        _store_eth.append(row)
        if _store_eth["price"].iloc[-1] > _store_eth["price"].iloc[-2]:
            #  we have a buy opportunity
            yield Trade(trade_type="BUY", base="ETH", volume=2)
        elif _store_eth["price"].iloc[-1] < _store_eth["price"].iloc[-2]:
            #  we have a sell opportunity
            yield Trade(trade_type="SELL", base="ETH", volume=2)
