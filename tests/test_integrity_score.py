"""Unit tests for Financial Integrity Score Calculator."""

import unittest
from backend.models.finding import (
    Finding,
    FindingStatus,
    Severity,
    SourceCitation,
    ProvenanceMetadata,
    CalculationVariance
)
from backend.verification.integrity_score import FinancialIntegrityScoreCalculator


class TestIntegrityScore(unittest.TestCase):

    def test_clean_system_score_is_100_a_plus(self):
        score, grade, breakdown = FinancialIntegrityScoreCalculator.calculate(
            findings=[],
            initial_capital=100_000.0,
            total_discrepancy=0.0
        )
        self.assertEqual(score, 100.0)
        self.assertEqual(grade, "A+")
        self.assertEqual(breakdown["critical_count"], 0)

    def test_critical_failure_deductions_lead_to_grade_f(self):
        finding = Finding(
            finding_id="F-001",
            title="Critical Sign Inversion",
            status=FindingStatus.CONTRADICTION,
            severity=Severity.CRITICAL,
            confidence=0.95,
            claim="Claimed profit on net loss",
            sources=[SourceCitation(file="strategy.py", line_range="1-10")],
            data_evidence=None,
            provenance=ProvenanceMetadata(timestamp="now", normalizer_version="v1", verifier_version="v1", transformation="t"),
            calculation=CalculationVariance(variance_amount=21960.0),
            verification_method="fifo",
            verifier_name="pnl",
            impact_level="HIGH",
            capital_at_risk=21960.0
        )

        score, grade, breakdown = FinancialIntegrityScoreCalculator.calculate(
            findings=[finding],
            initial_capital=100_000.0,
            total_discrepancy=21960.0
        )
        self.assertLess(score, 60.0)
        self.assertIn("critical_contradictions", breakdown["deductions"])


if __name__ == "__main__":
    unittest.main()
