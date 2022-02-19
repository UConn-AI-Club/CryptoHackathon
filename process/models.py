from dataclasses import dataclass

@dataclass
class Trade:
    trade_type: str # BUY | SELL
    base: str
    volume: Decimal
