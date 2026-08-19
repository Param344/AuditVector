"""Unit tests for ADK Tool wrappers."""

import os
import unittest
from backend.adk.tools import (
    sanitize_text,
    scan_repository_ast,
    load_normalized_trades,
    execute_trade_reconciliation,
    analyze_duckdb_dataset,
    evaluate_metric_variance,
    ADK_TOOL_REGISTRY
)


class TestADKTools(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.integritylab_dir = os.path.join(self.base_dir, "integritylab")
        self.data_file = os.path.join(self.integritylab_dir, "data", "trades_alpha_failure.csv")
        self.report_file = os.path.join(self.integritylab_dir, "reports", "alpha_performance_report.json")
        self.source_dir = os.path.join(self.integritylab_dir, "source")

    def test_tool_registry_contains_all_tools(self):
        self.assertEqual(len(ADK_TOOL_REGISTRY), 6)

    def test_sanitize_tool(self):
        res = sanitize_text('api_key = "AIzaSyD-1234567890abcdefghijklmn"')
        self.assertIn("[REDACTED]", res["sanitized_text"])
        self.assertEqual(res["redactions_performed"], 1)

    def test_scan_repository_ast_tool(self):
        res = scan_repository_ast(self.source_dir)
        self.assertIn("financial_modules", res)
        self.assertGreater(res["total_files"], 0)

    def test_load_normalized_trades_tool(self):
        res = load_normalized_trades(self.data_file)
        self.assertEqual(res["event_count"], 6)
        self.assertEqual(len(res["events"]), 6)

    def test_execute_trade_reconciliation_tool(self):
        res = execute_trade_reconciliation(self.data_file, self.report_file)
        self.assertIn("reconstructed_pnl", res)
        self.assertEqual(res["reconstructed_pnl"]["net_pnl"], -3720.0)

    def test_duckdb_tool(self):
        res = analyze_duckdb_dataset(self.data_file)
        self.assertEqual(res["total_records"], 6)
        self.assertEqual(res["unique_symbols"], 3)


if __name__ == "__main__":
    unittest.main()
