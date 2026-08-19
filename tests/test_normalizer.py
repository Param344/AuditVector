"""Unit tests for IngestionNormalizer."""

import unittest
from decimal import Decimal
from backend.ingestion.normalizer import IngestionNormalizer, NormalizationError
from backend.models.financial_event import OrderSide


class TestIngestionNormalizer(unittest.TestCase):

    def test_standard_columns(self):
        row = {
            "id": "T-100",
            "timestamp": "2026-01-01T10:00:00Z",
            "symbol": "BTC/USD",
            "side": "BUY",
            "quantity": "2.5",
            "price": "45000.00",
            "fee": "10.0",
            "fee_currency": "USD"
        }
        event = IngestionNormalizer.normalize_row(row, source="test.csv")
        self.assertEqual(event.event_id, "T-100")
        self.assertEqual(event.symbol, "BTC/USD")
        self.assertEqual(event.side, OrderSide.BUY)
        self.assertEqual(event.quantity, Decimal("2.5"))
        self.assertEqual(event.price, Decimal("45000.00"))
        self.assertEqual(event.fee, Decimal("10.0"))

    def test_alias_columns(self):
        # Using aliases like 'size', 'rate', 'commission'
        row = {
            "trade_id": "T-200",
            "time": "2026-01-02 12:30:00",
            "ticker": "eth-usdt",
            "action": "SELL",
            "size": "15.0",
            "rate": "$3,200.50",
            "commission": "$12.50"
        }
        event = IngestionNormalizer.normalize_row(row, source="test.csv")
        self.assertEqual(event.event_id, "T-200")
        self.assertEqual(event.symbol, "ETH-USDT")
        self.assertEqual(event.side, OrderSide.SELL)
        self.assertEqual(event.quantity, Decimal("15.0"))
        self.assertEqual(event.price, Decimal("3200.50"))
        self.assertEqual(event.fee, Decimal("12.50"))

    def test_missing_quantity_raises_error(self):
        row = {"price": "100.0", "symbol": "AAPL"}
        with self.assertRaises(NormalizationError):
            IngestionNormalizer.normalize_row(row)


if __name__ == "__main__":
    unittest.main()
