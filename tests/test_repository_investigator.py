"""Unit tests for RepositoryInvestigator AST analyzer."""

import os
import unittest
from backend.agents.repository_investigator import RepositoryInvestigator


class TestRepositoryInvestigator(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.source_dir = os.path.join(self.base_dir, "integritylab", "source")

    def test_ast_repository_mapping(self):
        calc_map = RepositoryInvestigator.analyze_repository(self.source_dir)
        self.assertGreater(calc_map["total_mapped_modules"], 0)
        
        modules = calc_map["modules"]
        # Must map strategy_alpha, fee_engine, control_strategy
        self.assertTrue(any("strategy_alpha.py" in m for m in modules))
        self.assertTrue(any("fee_engine.py" in m for m in modules))
        self.assertTrue(any("control_strategy.py" in m for m in modules))

        # Check detected functions and keywords
        alpha_meta = next(v for k, v in modules.items() if "strategy_alpha.py" in k)
        self.assertIn("calculate_portfolio_return", alpha_meta["functions"])
        self.assertIn("calculate_reported_pnl", alpha_meta["functions"])
        self.assertIn("pnl", alpha_meta["keywords"])
        self.assertIn("return", alpha_meta["keywords"])


if __name__ == "__main__":
    unittest.main()
