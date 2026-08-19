"""Unit tests for DuckDBVerificationEngine."""

import os
import unittest
from backend.verification.duckdb_engine import DuckDBVerificationEngine


class TestDuckDBEngine(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.csv_path = os.path.join(self.base_dir, "integritylab", "data", "trades_alpha_failure.csv")

    def test_duckdb_analysis(self):
        res = DuckDBVerificationEngine.analyze_events_with_duckdb(self.csv_path)
        self.assertEqual(res["total_records"], 6)
        self.assertEqual(res["unique_symbols"], 3)  # BTC, ETH, SOL
        self.assertEqual(len(res["symbol_stats"]), 3)


if __name__ == "__main__":
    unittest.main()
