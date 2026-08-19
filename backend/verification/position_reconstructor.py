"""Deterministic Position Reconstructor."""

from decimal import Decimal
from typing import List, Dict, Any
from ..models.financial_event import FinancialEvent, OrderSide


class PositionReconstructor:
    """Reconstructs historical open inventory, maximum exposure, and turnover."""
    VERSION = "position_reconstructor_v1.0"

    @classmethod
    def reconstruct_timeline(cls, events: List[FinancialEvent]) -> Dict[str, Any]:
        sorted_events = sorted(events, key=lambda e: e.timestamp)
        
        current_positions: Dict[str, Decimal] = {}
        max_notional_exposure = Decimal("0.0")
        total_turnover = Decimal("0.0")

        for ev in sorted_events:
            sym = ev.symbol
            if sym not in current_positions:
                current_positions[sym] = Decimal("0.0")

            if ev.side == OrderSide.BUY:
                current_positions[sym] += ev.quantity
            else:
                current_positions[sym] -= ev.quantity

            trade_notional = ev.quantity * ev.price
            total_turnover += trade_notional

            # Current total open notional rough estimate
            current_open_notional = sum(abs(q) * ev.price for q in current_positions.values())
            if current_open_notional > max_notional_exposure:
                max_notional_exposure = current_open_notional

        return {
            "final_positions": {k: float(v) for k, v in current_positions.items()},
            "max_notional_exposure": float(max_notional_exposure),
            "total_turnover": float(total_turnover),
            "event_count": len(events),
            "verifier_version": cls.VERSION
        }
