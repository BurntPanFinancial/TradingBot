from dataclasses import dataclass
from typing import Optional


@dataclass
class StrategySignal:
    """Normalized strategy output consumed by the backtest engine."""

    action: str
    size: int = 0
    reason: str = ""


@dataclass
class Position:
    """Current open position in a symbol."""

    quantity: int = 0
    average_price: float = 0.0


@dataclass
class Trade:
    """Executed trade record used for reporting and metrics."""

    timestamp: str
    symbol: str
    side: str
    quantity: int
    price: float
    fee: float
    pnl: Optional[float] = None
