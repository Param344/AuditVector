"""Unit tests for ReturnCalculator."""

import unittest
from backend.verification.return_calculator import ReturnCalculator


class TestReturnCalculator(unittest.TestCase):

    def test_positive_return(self):
        res = ReturnCalculator.calculate_return(
            initial_capital=100000.0,
            realized_pnl=5000.0,
            reported_return_pct=5.0
        )
        self.assertEqual(res["calculated_return_pct"], 5.0)
        self.assertFalse(res["polarity_contradiction"])

    def test_polarity_contradiction_detection(self):
        # Strategy lost -$3,720 (-3.72%) but system reports +18.24%
        res = ReturnCalculator.calculate_return(
            initial_capital=100000.0,
            realized_pnl=-3720.0,
            reported_return_pct=18.24
        )
        self.assertEqual(res["calculated_return_pct"], -3.72)
        self.assertTrue(res["polarity_contradiction"])


if __name__ == "__main__":
    unittest.main()
