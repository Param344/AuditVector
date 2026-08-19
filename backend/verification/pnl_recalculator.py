"""Deterministic Realized & Unrealized PnL Recalculator supporting Long & Short FIFO matching."""

from decimal import Decimal
from typing import List, Dict, Any, Tuple
from ..models.financial_event import FinancialEvent, OrderSide


class PnLRecalculator:
    """Bottom-up deterministic PnL reconstruction using FIFO matching for Longs and Shorts."""
    VERSION = "pnl_recalculator_v2.2"

    @classmethod
    def recalculate_fifo(cls, events: List[FinancialEvent]) -> Dict[str, Any]:
        """Calculates realized PnL, gross profit, gross loss, total fees, and net PnL."""
        if not events:
            return {
                "realized_pnl": 0.0,
                "gross_profit": 0.0,
                "gross_loss": 0.0,
                "total_fees": 0.0,
                "net_pnl": 0.0,
                "trade_count": 0,
                "closed_trades_count": 0,
                "open_quantity": 0.0,
                "verifier_version": cls.VERSION
            }

        # Sort events deterministically by timestamp, then event_id
        sorted_events = sorted(events, key=lambda e: (e.timestamp, e.event_id))

        # Inventory queue per symbol: list of dict(side, qty, price, event_id)
        symbol_queues: Dict[str, List[Dict[str, Any]]] = {}
        
        realized_pnl = Decimal("0.0")
        gross_profit = Decimal("0.0")
        gross_loss = Decimal("0.0")
        total_fees = Decimal("0.0")
        closed_trades = 0

        for event in sorted_events:
            total_fees += event.fee
            sym = event.symbol
            if sym not in symbol_queues:
                symbol_queues[sym] = []

            queue = symbol_queues[sym]
            incoming_qty = event.quantity
            incoming_side = event.side

            # If queue is empty or has same side lots, simply add to queue
            if not queue or queue[0]["side"] == incoming_side:
                queue.append({
                    "side": incoming_side,
                    "qty": incoming_qty,
                    "price": event.price,
                    "event_id": event.event_id
                })
            else:
                # Opposite side: match FIFO against existing queue
                while incoming_qty > Decimal("0.0") and len(queue) > 0:
                    open_lot = queue[0]
                    matched_qty = min(open_lot["qty"], incoming_qty)

                    if open_lot["side"] == OrderSide.BUY:
                        # Closing long position with incoming SELL
                        trade_pnl = (event.price - open_lot["price"]) * matched_qty
                    else:
                        # Closing short position with incoming BUY
                        trade_pnl = (open_lot["price"] - event.price) * matched_qty

                    realized_pnl += trade_pnl
                    if trade_pnl > Decimal("0.0"):
                        gross_profit += trade_pnl
                    elif trade_pnl < Decimal("0.0"):
                        gross_loss += abs(trade_pnl)

                    closed_trades += 1
                    open_lot["qty"] -= matched_qty
                    incoming_qty -= matched_qty

                    if open_lot["qty"] <= Decimal("0.0"):
                        queue.pop(0)

                # If any incoming quantity remains after closing existing lots, open new lot
                if incoming_qty > Decimal("0.0"):
                    queue.append({
                        "side": incoming_side,
                        "qty": incoming_qty,
                        "price": event.price,
                        "event_id": event.event_id
                    })

        net_pnl = realized_pnl - total_fees
        open_qty = sum(sum(lot["qty"] for lot in q) for q in symbol_queues.values())

        return {
            "realized_pnl": float(realized_pnl),
            "gross_profit": float(gross_profit),
            "gross_loss": float(gross_loss),
            "total_fees": float(total_fees),
            "net_pnl": float(net_pnl),
            "trade_count": len(events),
            "closed_trades_count": closed_trades,
            "open_quantity": float(open_qty),
            "verifier_version": cls.VERSION
        }
