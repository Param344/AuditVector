"""Integration tests for Google ADK Runner & Official ADK Agent objects."""

import os
import unittest
from google.adk.agents import Agent
from backend.adk.agents import FIVE_ADK_AGENTS, build_five_adk_agents
from backend.adk.runner import ADKRunner
from backend.models.finding import FindingStatus


class TestADKRunner(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.integritylab_dir = os.path.join(self.base_dir, "integritylab")
        self.source_dir = os.path.join(self.integritylab_dir, "source")
        self.data_alpha = os.path.join(self.integritylab_dir, "data", "trades_alpha_failure.csv")
        self.report_alpha = os.path.join(self.integritylab_dir, "reports", "alpha_performance_report.json")
        self.data_control = os.path.join(self.integritylab_dir, "data", "trades_control_case.csv")
        self.report_control = os.path.join(self.integritylab_dir, "reports", "control_performance_report.json")

    def test_official_google_adk_agent_objects(self):
        """Confirms that all 5 agents are instances of google.adk.agents.Agent."""
        agents = build_five_adk_agents("gemini-3.5-flash")
        self.assertEqual(len(agents), 5)
        
        expected_names = [
            "AuditPlanner",
            "RepositoryInvestigator",
            "FinancialInvestigator",
            "ContradictionInvestigator",
            "ReportAgent"
        ]
        for name in expected_names:
            agent = next(a for a in agents.values() if a.name == name)
            self.assertIsInstance(agent, Agent)
            self.assertEqual(agent.model, "gemini-3.5-flash")
            self.assertTrue(len(agent.tools) > 0 or name == "ReportAgent")

    def test_adk_runner_alpha_pipeline(self):
        res = ADKRunner.run_audit(
            audit_id="adk-test-alpha",
            project_name="IntegrityLab-Alpha",
            repo_path=self.source_dir,
            data_file=self.data_alpha,
            report_file=self.report_alpha
        )

        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(res["audit_id"], "adk-test-alpha")
        self.assertEqual(res["gemini_model"], "gemini-3.5-flash")
        self.assertIn("agent_pipeline", res)
        
        # Verify all 5 agents executed in pipeline
        pipeline = res["agent_pipeline"]
        self.assertIsNotNone(pipeline["planner"])
        self.assertIsNotNone(pipeline["repository_investigator"])
        self.assertIsNotNone(pipeline["financial_investigator"])
        self.assertIsNotNone(pipeline["contradiction_investigator"])
        self.assertIsNotNone(pipeline["report_agent"])

        # Check execution logs for agent stage tracking
        logs = res["execution_logs"]
        agents_logged = {l["agent_name"] for l in logs}
        self.assertIn("AuditPlanner", agents_logged)
        self.assertIn("RepositoryInvestigator", agents_logged)
        self.assertIn("FinancialInvestigator", agents_logged)
        self.assertIn("ContradictionInvestigator", agents_logged)
        self.assertIn("ReportAgent", agents_logged)

        # Check findings (4 known failures)
        findings = pipeline["contradiction_investigator"]
        self.assertEqual(len(findings), 4)

    def test_adk_runner_control_pipeline(self):
        res = ADKRunner.run_audit(
            audit_id="adk-test-control",
            project_name="IntegrityLab-Control",
            repo_path=self.source_dir,
            data_file=self.data_control,
            report_file=self.report_control
        )

        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(res["report"]["verdict"], "✅ FINANCIAL INTEGRITY VERIFIED")
        self.assertEqual(len(res["agent_pipeline"]["contradiction_investigator"]), 1)
        self.assertEqual(res["agent_pipeline"]["contradiction_investigator"][0]["status"], FindingStatus.VERIFIED.value)


if __name__ == "__main__":
    unittest.main()
