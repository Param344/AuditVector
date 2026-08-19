"""Unit tests for FinancialInvestigator claim extractor."""

import unittest
from backend.agents.financial_investigator import FinancialInvestigator


class TestFinancialInvestigator(unittest.TestCase):

    def test_extract_claims_from_reports_and_config(self):
        reported_metrics = {
            "reported_pnl": 18240.0,
            "reported_return_pct": 18.24,
            "reported_fees": 440.0,
            "file_path": "report.json"
        }
        config_data = {
            "model_assumptions": {
                "fee_model_bps": 5.0
            }
        }
        claims = FinancialInvestigator.extract_claims(reported_metrics, config_data)
        self.assertEqual(len(claims), 4)
        
        claim_types = [c.claim_type for c in claims]
        self.assertIn("REALIZED_PNL", claim_types)
        self.assertIn("RETURN_PERCENTAGE", claim_types)
        self.assertIn("TOTAL_FEES", claim_types)
        self.assertIn("CONFIGURED_FEE_BPS", claim_types)


if __name__ == "__main__":
    unittest.main()
