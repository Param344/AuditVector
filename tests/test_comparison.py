"""Forensic Unit Tests for ComparisonEngine covering all 4 FindingStatus categories."""

import unittest
from backend.models.finding import FindingStatus, Severity
from backend.verification.comparison import ComparisonEngine


class TestComparisonEngineForensics(unittest.TestCase):

    def test_exact_match(self):
        res = ComparisonEngine.evaluate_variance("PnL", 10000.0, 10000.0)
        self.assertEqual(res["status"], FindingStatus.VERIFIED)
        self.assertEqual(res["variance"], 0.0)

    def test_within_tolerance(self):
        # 0.2% variance (within default 1% tolerance)
        res = ComparisonEngine.evaluate_variance("PnL", 10020.0, 10000.0)
        self.assertEqual(res["status"], FindingStatus.VERIFIED)

    def test_material_mismatch_contradiction(self):
        # 25% discrepancy
        res = ComparisonEngine.evaluate_variance("PnL", 12500.0, 10000.0)
        self.assertEqual(res["status"], FindingStatus.CONTRADICTION)
        self.assertEqual(res["severity"], Severity.HIGH)
        self.assertEqual(res["variance"], 2500.0)

    def test_polarity_inversion_critical_contradiction(self):
        # Positive vs Negative
        res = ComparisonEngine.evaluate_variance("Return", 15.0, -3.5)
        self.assertEqual(res["status"], FindingStatus.CONTRADICTION)
        self.assertEqual(res["severity"], Severity.CRITICAL)

    def test_insufficient_evidence_unverifiable(self):
        # Missing reported or reconstructed value
        res = ComparisonEngine.evaluate_variance("Exit Fees", None, 150.0)
        self.assertEqual(res["status"], FindingStatus.UNVERIFIABLE)
        self.assertIn("Missing value", res["reason"])

        res2 = ComparisonEngine.evaluate_variance("PnL", 5000.0, None)
        self.assertEqual(res2["status"], FindingStatus.UNVERIFIABLE)


if __name__ == "__main__":
    unittest.main()
