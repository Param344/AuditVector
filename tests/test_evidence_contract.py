"""Unit tests for Evidence Contract validation rule."""

import unittest
from backend.models.finding import (
    Finding, FindingStatus, Severity, SourceCitation,
    ProvenanceMetadata, CalculationVariance
)
from backend.evidence.evidence_store import EvidenceStore


class TestEvidenceContract(unittest.TestCase):

    def test_no_evidence_contract_raises_error(self):
        # A finding claiming CONTRADICTION but having empty sources should fail contract
        invalid_finding = Finding(
            finding_id="F-999",
            title="Unproven claim",
            status=FindingStatus.CONTRADICTION,
            severity=Severity.HIGH,
            confidence=0.9,
            claim="Unbacked claim",
            sources=[],  # Empty sources violates Evidence Contract!
            data_evidence=None,
            provenance=ProvenanceMetadata("2026-01-01T00:00:00Z", "v1.0", "v1.0", "test"),
            calculation=CalculationVariance(),
            verification_method="none",
            verifier_name="none",
            impact_level="LOW"
        )
        self.assertFalse(invalid_finding.validate_contract())

        store = EvidenceStore()
        with self.assertRaises(ValueError):
            store.add_finding(invalid_finding)

    def test_valid_evidence_contract_accepted(self):
        valid_finding = Finding(
            finding_id="F-100",
            title="Verified Contradiction",
            status=FindingStatus.CONTRADICTION,
            severity=Severity.HIGH,
            confidence=0.95,
            claim="Proven discrepancy",
            sources=[SourceCitation("logic.py", "10-20", "hash123")],
            data_evidence=None,
            provenance=ProvenanceMetadata("2026-01-01T00:00:00Z", "v1.0", "v1.0", "test"),
            calculation=CalculationVariance(reported_pnl=100.0, reconstructed_pnl=50.0),
            verification_method="recalculation",
            verifier_name="pnl_recalculator",
            impact_level="MEDIUM"
        )
        self.assertTrue(valid_finding.validate_contract())
        store = EvidenceStore()
        self.assertTrue(store.add_finding(valid_finding))


if __name__ == "__main__":
    unittest.main()
