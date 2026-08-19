"""Trade & Performance Reconciler."""

from typing import List, Dict, Any, Optional
from ..models.financial_event import FinancialEvent
from .pnl_recalculator import PnLRecalculator
from .fee_recalculator import FeeRecalculator
from .return_calculator import ReturnCalculator


class TradeReconciler:
    """Master reconciler that ties trade fills, reports, and code expectations together."""
    VERSION = "trade_reconciler_v1.0"

    @classmethod
    def reconcile(
        cls,
        events: List[FinancialEvent],
        reported_metrics: Dict[str, Any],
        initial_capital: float = 100_000.0,
        expected_fee_bps: Optional[float] = None
    ) -> Dict[str, Any]:

        pnl_results = PnLRecalculator.recalculate_fifo(events)
        
        reported_pnl = reported_metrics.get("reported_pnl") or reported_metrics.get("pnl") or reported_metrics.get("net_pnl")
        reported_return = reported_metrics.get("reported_return_pct") or reported_metrics.get("return_pct") or reported_metrics.get("return")
        reported_fees = reported_metrics.get("reported_fees") or reported_metrics.get("fees") or reported_metrics.get("total_fees")

        fee_results = FeeRecalculator.analyze_fees(
            events, 
            expected_bps=expected_fee_bps, 
            reported_total_fees=float(reported_fees) if reported_fees is not None else None
        )

        return_results = ReturnCalculator.calculate_return(
            initial_capital=initial_capital,
            realized_pnl=pnl_results["net_pnl"],
            reported_return_pct=float(reported_return) if reported_return is not None else None
        )

        pnl_variance = None
        if reported_pnl is not None:
            pnl_variance = float(reported_pnl) - pnl_results["net_pnl"]

        return {
            "reconstructed_pnl": pnl_results,
            "fee_analysis": fee_results,
            "return_analysis": return_results,
            "pnl_variance": pnl_variance,
            "reported_metrics": reported_metrics,
            "verifier_version": cls.VERSION
        }
