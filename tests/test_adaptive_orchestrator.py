"""Unit tests for AdaptiveAuditOrchestrator and AuditMission lifecycle."""

import unittest
from backend.adk.orchestrator import AdaptiveAuditOrchestrator
from backend.models.mission import MissionStatus, MissionStage


class TestAdaptiveOrchestrator(unittest.TestCase):

    def test_alpha_mission_adaptive_routing_and_remediation(self):
        mission = AdaptiveAuditOrchestrator.execute_mission(
            mission_id="mission-test-alpha",
            target_system="IntegrityLab-Alpha",
            repo_path="integritylab/source",
            data_file="integritylab/data/trades_alpha_failure.csv",
            report_file="integritylab/reports/alpha_performance_report.json",
            claimed_fee_bps=5.0
        )
        self.assertEqual(mission.status, MissionStatus.COMPLETED)
        self.assertEqual(mission.stage, MissionStage.VERDICT_SEALED)
        self.assertGreater(len(mission.findings), 0)
        self.assertGreater(len(mission.adaptive_decisions), 3)
        self.assertGreater(len(mission.replay_snapshots), 4)
        self.assertGreater(len(mission.remediation_plans), 0)
        self.assertLess(mission.financial_integrity_score, 50.0)
        self.assertEqual(mission.integrity_grade, "F")

    def test_control_mission_clean_baseline_score(self):
        mission = AdaptiveAuditOrchestrator.execute_mission(
            mission_id="mission-test-control",
            target_system="IntegrityLab-Control",
            repo_path="integritylab/source",
            data_file="integritylab/data/trades_control_case.csv",
            report_file="integritylab/reports/control_performance_report.json",
            claimed_fee_bps=5.0
        )
        self.assertEqual(mission.status, MissionStatus.COMPLETED)
        self.assertEqual(mission.total_capital_at_risk, 0.0)
        self.assertEqual(mission.financial_integrity_score, 100.0)
        self.assertEqual(mission.integrity_grade, "A+")


if __name__ == "__main__":
    unittest.main()
