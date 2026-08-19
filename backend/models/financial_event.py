"""Canonical Financial Event & Ingestion Models for AuditVector."""

from dataclasses import dataclass, field, asdict
from decimal import Decimal
from enum import Enum
from typing import Optional, Dict, Any, List
import datetime
import hashlib
import json


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class FinancialEvent:
    """Canonical representation of any execution/trade transaction."""
    event_id: str
    timestamp: str  # ISO 8601 UTC string
    symbol: str
    side: OrderSide
    quantity: Decimal
    price: Decimal
    fee: Decimal = Decimal("0.0")
    fee_currency: str = "USD"
    position_id: Optional[str] = None
    trade_id: Optional[str] = None
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["side"] = self.side.value if isinstance(self.side, OrderSide) else str(self.side)
        data["quantity"] = float(self.quantity)
        data["price"] = float(self.price)
        data["fee"] = float(self.fee)
        return data

    def compute_hash(self) -> str:
        serialized = f"{self.event_id}:{self.timestamp}:{self.symbol}:{self.side.value}:{self.quantity}:{self.price}:{self.fee}"
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
