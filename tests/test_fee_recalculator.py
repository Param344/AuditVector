"""Unit tests for FeeRecalculator."""

import unittest
from decimal import Decimal
from backend.models.financial_event import FinancialEvent, OrderSide
from backend.verification.fee_recalculator import FeeRecalculator


class TestFeeRecalculator(unittest.TestCase):

    def test_fee_double_count_detection(self):
        events = [
            FinancialEvent("1", "2026-01-01T00:00:00Z", "BTC", OrderSide.BUY, Decimal("1.0"), Decimal("50000.0"), Decimal("60.0")),
            FinancialEvent("2", "2026-01-02T00:00:00Z", "BTC", OrderSide.SELL, Decimal("1.0"), Decimal("48000.0"), Decimal("50.0")),
        ]
        # Sum of trade fees = 110. Reported = 220 (double counted)
        res = FeeRecalculator.analyze_fees(events, reported_total_fees=220.0)
        self.assertEqual(res["calculated_fees"], 110.0)
        self.assertTrue(res["double_count_detected"])
        self.assertEqual(res["double_count_variance"], 110.0)


if __name__ == "__main__":
    unittest.main()
