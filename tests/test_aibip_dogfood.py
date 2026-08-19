"""Unit and Integration Tests for Real-World AI-BIP Quantitative Strategy Dogfooding."""

import os
import time
import unittest
from fastapi.testclient import TestClient
from backend.api.server import app
from backend.adk.runner import ADKRunner


class TestAIBIPDogfood(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dogfood_dir = os.path.join(self.base_dir, "dogfood", "aibip")
        self.source_dir = os.path.join(self.dogfood_dir, "source")
        self.data_file = os.path.join(self.dogfood_dir, "data", "trades_aibip_real.csv")
        self.report_file = os.path.join(self.dogfood_dir, "reports", "aibip_performance_report.json")
        self.client = TestClient(app)

    def test_aibip_dogfood_adk_audit(self):
        """Audits real-world AI-BIP quantitative system and proves PnL/return discrepancy."""
        res = ADKRunner.run_audit(
            audit_id="adk-aibip-dogfood",
            project_name="AI-BIP-Quant-Dogfood",
            repo_path=self.source_dir,
            data_file=self.data_file,
            report_file=self.report_file,
            claimed_fee_bps=8.0
        )

        self.assertEqual(res["status"], "COMPLETED")
        report = res["report"]
        self.assertIn("⚠️", report["verdict"])

        findings = report["findings"]
        self.assertGreater(len(findings), 0)

        # Confirm PnL reconciliation contradiction
        pnl_finding = next((f for f in findings if "PnL Reconciliation" in f["title"]), None)
        self.assertIsNotNone(pnl_finding)
        self.assertEqual(pnl_finding["status"], "CONTRADICTION")
        self.assertEqual(pnl_finding["severity"], "HIGH")
        self.assertEqual(pnl_finding["calculation"]["reported_pnl"], 54200.0)
        self.assertAlmostEqual(pnl_finding["calculation"]["reconstructed_pnl"], 37913.76, places=2)

    def test_aibip_demo_api_lifecycle(self):
        response = self.client.post("/api/audits/demo/aibip")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("audit_id", data)
        audit_id = data["audit_id"]

        # Poll status
        for _ in range(25):
            status_res = self.client.get(f"/api/audits/{audit_id}")
            self.assertEqual(status_res.status_code, 200)
            status_data = status_res.json()
            if status_data["stage"] == "COMPLETED":
                break
            time.sleep(0.05)

        self.assertEqual(status_data["stage"], "COMPLETED")
        self.assertIsNotNone(status_data["result"])
        self.assertIn("⚠️", status_data["result"]["report"]["verdict"])


if __name__ == "__main__":
    unittest.main()
