"""Unit tests for AuditVector Remediation Sandbox & Patch Generator."""

import unittest
from backend.models.finding import (
    Finding,
    FindingStatus,
    Severity,
    SourceCitation,
    ProvenanceMetadata,
    CalculationVariance
)
from backend.models.remediation import PatchStatus
from backend.models.financial_event import FinancialEvent
from backend.remediation.patch_generator import PatchGenerator
from backend.remediation.sandbox import RemediationSandbox


class TestRemediationSandbox(unittest.TestCase):

    def setUp(self):
        self.finding_pnl = Finding(
            finding_id="F-001",
            title="PnL Sign Inversion Failure",
            status=FindingStatus.CONTRADICTION,
            severity=Severity.CRITICAL,
            confidence=0.98,
            claim="System reported Net PnL +$18,240.00",
            sources=[SourceCitation(file="strategy_alpha.py", line_range="18-26")],
            data_evidence=None,
            provenance=ProvenanceMetadata(
                timestamp="2026-08-21T00:00:00Z",
                normalizer_version="v1.2",
                verifier_version="pnl_recalculator_v2.2",
                transformation="fifo"
            ),
            calculation=CalculationVariance(
                reported_pnl=18240.0,
                reconstructed_pnl=-3720.0,
                variance_amount=21960.0
            ),
            verification_method="deterministic_fifo_recalculation",
            verifier_name="pnl_recalculator_v2.2",
            impact_level="CRITICAL",
            capital_at_risk=21960.0
        )

        self.sample_events = [
            FinancialEvent(event_id="e1", timestamp="2026-01-01", symbol="AAPL", side="BUY", quantity=100.0, price=150.0, fee=10.0),
            FinancialEvent(event_id="e2", timestamp="2026-01-02", symbol="AAPL", side="SELL", quantity=100.0, price=145.0, fee=10.0)
        ]

    def test_patch_generation_pnl_inversion(self):
        plan = PatchGenerator.generate_patch_for_finding(self.finding_pnl, "integritylab/source")
        self.assertIsNotNone(plan)
        self.assertEqual(plan.finding_id, "F-001")
        self.assertEqual(plan.issue_type, "SIGN_INVERSION")
        self.assertIn("--- a/strategy_alpha.py", plan.unified_diff)
        self.assertTrue(plan.human_approval_required)
        self.assertFalse(plan.applied_to_repo)

    def test_isolated_sandbox_verification_reduces_discrepancy(self):
        plan = PatchGenerator.generate_patch_for_finding(self.finding_pnl, "integritylab/source")
        verified_plan = RemediationSandbox.verify_patch(
            plan=plan,
            finding=self.finding_pnl,
            events=self.sample_events,
            initial_capital=100_000.0
        )
        self.assertEqual(verified_plan.status, PatchStatus.VERIFIED_SOUND)
        self.assertIsNotNone(verified_plan.verification_metrics)
        self.assertEqual(verified_plan.verification_metrics.post_patch_discrepancy, 0.0)
        self.assertTrue(verified_plan.verification_metrics.discrepancy_resolved)
        self.assertGreater(verified_plan.verification_metrics.tests_passed, 0)

    def test_patch_application_blocked_without_human_authorization(self):
        plan = PatchGenerator.generate_patch_for_finding(self.finding_pnl, "integritylab/source")
        success, msg = RemediationSandbox.apply_patch_with_human_authorization(
            plan=plan,
            repo_path="integritylab/source",
            authorized_by_human=False
        )
        self.assertFalse(success)
        self.assertIn("BLOCKED", msg)


if __name__ == "__main__":
    unittest.main()
