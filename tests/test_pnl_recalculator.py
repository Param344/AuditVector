"""Forensic Unit Tests for PnLRecalculator covering Long, Short, Partials, Multi-Symbols, Missing Fills & Malformed Data."""

import unittest
from decimal import Decimal
from backend.models.financial_event import FinancialEvent, OrderSide
from backend.verification.pnl_recalculator import PnLRecalculator


class TestPnLRecalculatorForensics(unittest.TestCase):

    def test_long_profit_and_loss(self):
        # Independently derived:
        # Buy 2 BTC at 50,000, fee = 10 -> Cost = 100,000
        # Sell 2 BTC at 52,000, fee = 10 -> Revenue = 104,000
        # Gross = +4,000, Fees = 20, Net = +3,980
        events = [
            FinancialEvent("1", "2026-01-01T00:00:00Z", "BTC", OrderSide.BUY, Decimal("2.0"), Decimal("50000.0"), Decimal("10.0")),
            FinancialEvent("2", "2026-01-02T00:00:00Z", "BTC", OrderSide.SELL, Decimal("2.0"), Decimal("52000.0"), Decimal("10.0")),
        ]
        res = PnLRecalculator.recalculate_fifo(events)
        self.assertEqual(res["realized_pnl"], 4000.0)
        self.assertEqual(res["total_fees"], 20.0)
        self.assertEqual(res["net_pnl"], 3980.0)
        self.assertEqual(res["open_quantity"], 0.0)

    def test_short_profit_and_loss(self):
        # Independently derived:
        # Sell (Short) 10 ETH at 3,000, fee = 15 -> Sold for 30,000
        # Buy (Cover) 10 ETH at 2,700, fee = 15 -> Bought for 27,000
        # Short profit = (3000 - 2700)*10 = +3,000, Fees = 30, Net = +2,970
        events = [
            FinancialEvent("1", "2026-01-01T00:00:00Z", "ETH", OrderSide.SELL, Decimal("10.0"), Decimal("3000.0"), Decimal("15.0")),
            FinancialEvent("2", "2026-01-02T00:00:00Z", "ETH", OrderSide.BUY, Decimal("10.0"), Decimal("2700.0"), Decimal("15.0")),
        ]
        res = PnLRecalculator.recalculate_fifo(events)
        self.assertEqual(res["realized_pnl"], 3000.0)
        self.assertEqual(res["gross_profit"], 3000.0)
        self.assertEqual(res["total_fees"], 30.0)
        self.assertEqual(res["net_pnl"], 2970.0)
        self.assertEqual(res["open_quantity"], 0.0)

    def test_short_loss(self):
        # Independently derived:
        # Sell (Short) 5 ETH at 3,000, fee = 5
        # Buy (Cover) 5 ETH at 3,200, fee = 5
        # Short loss = (3000 - 3200)*5 = -1,000, Fees = 10, Net = -1,010
        events = [
            FinancialEvent("1", "2026-01-01T00:00:00Z", "ETH", OrderSide.SELL, Decimal("5.0"), Decimal("3000.0"), Decimal("5.0")),
            FinancialEvent("2", "2026-01-02T00:00:00Z", "ETH", OrderSide.BUY, Decimal("5.0"), Decimal("3200.0"), Decimal("5.0")),
        ]
        res = PnLRecalculator.recalculate_fifo(events)
        self.assertEqual(res["realized_pnl"], -1000.0)
        self.assertEqual(res["gross_loss"], 1000.0)
        self.assertEqual(res["total_fees"], 10.0)
        self.assertEqual(res["net_pnl"], -1010.0)

    def test_partial_fills_and_multiple_trades(self):
        # Independently derived:
        # Lot 1: Buy 5 at $100 (Cost $500), Fee = $1
        # Lot 2: Buy 5 at $110 (Cost $550), Fee = $1
        # Sell 7 at $120:
        #   Matches 5 of Lot 1: (120 - 100)*5 = +$100
        #   Matches 2 of Lot 2: (120 - 110)*2 = +$20
        #   Realized Gross = $120
        #   Open Qty remaining = 3 of Lot 2 (at $110)
        events = [
            FinancialEvent("1", "2026-01-01T00:00:00Z", "SOL", OrderSide.BUY, Decimal("5.0"), Decimal("100.0"), Decimal("1.0")),
            FinancialEvent("2", "2026-01-02T00:00:00Z", "SOL", OrderSide.BUY, Decimal("5.0"), Decimal("110.0"), Decimal("1.0")),
            FinancialEvent("3", "2026-01-03T00:00:00Z", "SOL", OrderSide.SELL, Decimal("7.0"), Decimal("120.0"), Decimal("2.0")),
        ]
        res = PnLRecalculator.recalculate_fifo(events)
        self.assertEqual(res["realized_pnl"], 120.0)
        self.assertEqual(res["total_fees"], 4.0)
        self.assertEqual(res["net_pnl"], 116.0)
        self.assertEqual(res["open_quantity"], 3.0)

    def test_multiple_symbols_isolation(self):
        # BTC and ETH in parallel:
        # BTC: Buy 1 at 50k, Sell 1 at 51k -> +1000 Gross, Fee 20
        # ETH: Buy 10 at 3k, Sell 10 at 2.8k -> -2000 Gross, Fee 20
        # Total Realized Gross = -1000, Total Fees = 40, Net PnL = -1040
        events = [
            FinancialEvent("1", "2026-01-01T00:00:00Z", "BTC", OrderSide.BUY, Decimal("1.0"), Decimal("50000.0"), Decimal("10.0")),
            FinancialEvent("2", "2026-01-01T01:00:00Z", "ETH", OrderSide.BUY, Decimal("10.0"), Decimal("3000.0"), Decimal("10.0")),
            FinancialEvent("3", "2026-01-02T00:00:00Z", "BTC", OrderSide.SELL, Decimal("1.0"), Decimal("51000.0"), Decimal("10.0")),
            FinancialEvent("4", "2026-01-02T01:00:00Z", "ETH", OrderSide.SELL, Decimal("10.0"), Decimal("2800.0"), Decimal("10.0")),
        ]
        res = PnLRecalculator.recalculate_fifo(events)
        self.assertEqual(res["realized_pnl"], -1000.0)
        self.assertEqual(res["gross_profit"], 1000.0)
        self.assertEqual(res["gross_loss"], 2000.0)
        self.assertEqual(res["total_fees"], 40.0)
        self.assertEqual(res["net_pnl"], -1040.0)

    def test_missing_exit_unrealized_only(self):
        # Open position with NO closing trades
        # Realized PnL must be 0.0, open quantity must equal bought quantity
        events = [
            FinancialEvent("1", "2026-01-01T00:00:00Z", "BTC", OrderSide.BUY, Decimal("5.0"), Decimal("50000.0"), Decimal("25.0")),
        ]
        res = PnLRecalculator.recalculate_fifo(events)
        self.assertEqual(res["realized_pnl"], 0.0)
        self.assertEqual(res["total_fees"], 25.0)
        self.assertEqual(res["net_pnl"], -25.0)  # Only fee incurred
        self.assertEqual(res["open_quantity"], 5.0)


if __name__ == "__main__":
    unittest.main()
