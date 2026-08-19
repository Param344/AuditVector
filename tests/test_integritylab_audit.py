"""End-to-end integration test of AuditWorker on IntegrityLab synthetic dataset."""

import os
import unittest
from backend.workers.audit_worker import AuditWorker
from backend.models.finding import FindingStatus, Severity


class TestIntegrityLabAudit(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.integritylab_dir = os.path.join(self.base_dir, "integritylab")
        self.source_dir = os.path.join(self.integritylab_dir, "source")
        self.data_alpha = os.path.join(self.integritylab_dir, "data", "trades_alpha_failure.csv")
        self.report_alpha = os.path.join(self.integritylab_dir, "reports", "alpha_performance_report.json")
        
        self.data_control = os.path.join(self.integritylab_dir, "data", "trades_control_case.csv")
        self.report_control = os.path.join(self.integritylab_dir, "reports", "control_performance_report.json")

    def test_alpha_failure_audit(self):
        """Audit of IntegrityLab Alpha must confirm exactly all 4 planted integrity contradictions/warnings."""
        audit_res = AuditWorker.execute_audit(
            project_name="IntegrityLab-Alpha-Audit",
            repo_path=self.source_dir,
            data_file=self.data_alpha,
            report_file=self.report_alpha,
            claimed_fee_bps=5.0
        )

        self.assertEqual(audit_res["status"], "COMPLETED")
        report = audit_res["report"]
        self.assertIn("⚠️", report["verdict"])
        
        findings = report["findings"]
        # Expected: exactly 4 planted failures (PnL fail, Return polarity, Fee double-count, Config fee rate mismatch)
        self.assertEqual(len(findings), 4)
        
        # Verify specific failure categories
        titles = [f["title"] for f in findings]
        self.assertTrue(any("PnL Reconciliation" in t for t in titles))
        self.assertTrue(any("Return Polarity" in t for t in titles))
        self.assertTrue(any("Fee Double-Counting" in t for t in titles))
        self.assertTrue(any("Fee Model Rate Mismatch" in t for t in titles))

        # Check severities
        self.assertEqual(report["summary_counts"]["critical"], 2)  # PnL + Polarity
        self.assertEqual(report["summary_counts"]["high"], 1)      # Double counting
        self.assertEqual(report["summary_counts"]["medium"], 1)    # Config mismatch
        self.assertEqual(report["summary_counts"]["low"], 0)

    def test_control_case_audit(self):
        """Audit of IntegrityLab Control must verify 100% calculation soundness with 0 false contradictions."""
        audit_res = AuditWorker.execute_audit(
            project_name="IntegrityLab-Control-Audit",
            repo_path=self.source_dir,
            data_file=self.data_control,
            report_file=self.report_control,
            claimed_fee_bps=5.0
        )

        self.assertEqual(audit_res["status"], "COMPLETED")
        report = audit_res["report"]
        self.assertEqual(report["verdict"], "✅ FINANCIAL INTEGRITY VERIFIED")
        
        findings = report["findings"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["status"], FindingStatus.VERIFIED.value)
        self.assertEqual(report["summary_counts"]["critical"], 0)
        self.assertEqual(report["summary_counts"]["high"], 0)
        self.assertEqual(report["summary_counts"]["medium"], 0)
        self.assertEqual(report["summary_counts"]["low"], 1)


if __name__ == "__main__":
    unittest.main()
