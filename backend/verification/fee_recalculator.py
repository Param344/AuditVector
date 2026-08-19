"""Deterministic Fee Recalculator & Double-Count Detector."""

from decimal import Decimal
from typing import List, Dict, Any, Optional
from ..models.financial_event import FinancialEvent


class FeeRecalculator:
    """Verifies fee deduction logic and identifies fee double-counting anomalies."""
    VERSION = "fee_recalculator_v1.0"

    @classmethod
    def analyze_fees(
        cls, 
        events: List[FinancialEvent], 
        expected_bps: Optional[float] = None,
        reported_total_fees: Optional[float] = None
    ) -> Dict[str, Any]:
        
        summed_fees = Decimal("0.0")
        total_notional = Decimal("0.0")

        for event in events:
            summed_fees += event.fee
            notional = event.quantity * event.price
            total_notional += notional

        calculated_fees_from_events = float(summed_fees)
        effective_bps = (float(summed_fees) / float(total_notional) * 10000.0) if total_notional > Decimal("0") else 0.0

        double_count_detected = False
        double_count_variance = 0.0

        if reported_total_fees is not None:
            # If reported fees is approx 2x of summed trade fees
            ratio = reported_total_fees / calculated_fees_from_events if calculated_fees_from_events > 0 else 0
            if 1.90 <= ratio <= 2.10:
                double_count_detected = True
                double_count_variance = reported_total_fees - calculated_fees_from_events

        model_fee_variance = None
        if expected_bps is not None and total_notional > Decimal("0"):
            expected_fee_amount = float(total_notional) * (expected_bps / 10000.0)
            model_fee_variance = calculated_fees_from_events - expected_fee_amount

        return {
            "total_notional": float(total_notional),
            "calculated_fees": calculated_fees_from_events,
            "effective_bps": effective_bps,
            "reported_fees": reported_total_fees,
            "double_count_detected": double_count_detected,
            "double_count_variance": double_count_variance,
            "model_fee_variance": model_fee_variance,
            "verifier_version": cls.VERSION
        }
