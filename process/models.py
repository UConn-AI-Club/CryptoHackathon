from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Trade:
    trade_type: str # BUY | SELL
    base: str
    volume: Decimal
