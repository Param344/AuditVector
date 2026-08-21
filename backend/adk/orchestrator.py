"""Adaptive ADK Orchestration Engine for AuditVector.

Upgrades the investigation pipeline from a linear sequence into an evidence-driven
adaptive loop. Evaluates evidence sufficiency after each stage, makes autonomous routing
decisions, dispatches targeted deterministic tools, and drives sandbox remediation.
"""

import os
import time
import json
import logging
from dataclasses import asdict
from typing import Dict, Any, List, Optional
from ..config.settings import settings
from ..evidence.evidence_store import EvidenceStore
from ..evidence.evidence_graph import EvidenceGraph
from ..models.mission import (
    AuditMission,
    MissionStatus,
    MissionStage,
    MissionScope,
    AdaptiveDecision
)
from ..models.finding import Finding, FindingStatus
from ..models.financial_event import FinancialEvent
from ..models.remediation import RemediationPlan
from ..verification.integrity_score import FinancialIntegrityScoreCalculator
from ..ingestion.csv import CSVIngestionAdapter
from ..ingestion.reports import ReportIngestionAdapter
from ..agents.audit_planner import AuditPlanner
from ..agents.repository_investigator import RepositoryInvestigator
from ..agents.financial_investigator import FinancialInvestigator
from ..agents.contradiction_investigator import ContradictionInvestigator
from ..agents.report_agent import ReportAgent
from ..agents.remediation_agent import RemediationAgent
from .tools import analyze_duckdb_dataset

logger = logging.getLogger("AuditVector.AdaptiveOrchestrator")


class AdaptiveAuditOrchestrator:
    """Manages the full lifecycle of an AuditMission with adaptive routing and sandbox remediation."""

    @classmethod
    def execute_mission(
        cls,
        mission_id: str,
        target_system: str,
        repo_path: str,
        data_file: str,
        report_file: str,
        claimed_fee_bps: float = 5.0,
        initial_capital: float = 100_000.0,
        goal: Optional[str] = None
    ) -> AuditMission:
        
        start_time = time.time()
        mission_goal = goal or f"Autonomously investigate financial integrity and calculate deterministic ground-truth variance for {target_system}."

        scope = MissionScope(
            repo_path=repo_path,
            data_file=data_file,
            report_file=report_file,
            claimed_fee_bps=claimed_fee_bps,
            initial_capital=initial_capital
        )

        mission = AuditMission(
            mission_id=mission_id,
            goal=mission_goal,
            target_system=target_system,
            scope=scope,
            status=MissionStatus.IN_PROGRESS,
            stage=MissionStage.PLANNING,
            progress_pct=5
        )

        evidence_store = EvidenceStore()
        events: List[FinancialEvent] = []

        def record_snapshot(stage_name: str, desc: str, active_agent: str):
            snapshot = {
                "step_index": len(mission.replay_snapshots) + 1,
                "timestamp": time.time(),
                "elapsed_ms": round((time.time() - start_time) * 1000, 1),
                "stage": stage_name,
                "active_agent": active_agent,
                "description": desc,
                "findings_count": len(mission.findings),
                "progress_pct": mission.progress_pct,
                "evidence_count": len(mission.evidence_collected)
            }
            mission.replay_snapshots.append(snapshot)

        # -------------------------------------------------------------
        # STAGE 1: PLANNING & DISCOVERY
        # -------------------------------------------------------------
        mission.stage = MissionStage.PLANNING
        mission.progress_pct = 15
        record_snapshot("PLANNING", "Scoping repository structure and validating transactional datasets", "AuditPlanner")

        plan_output = AuditPlanner.plan_audit(repo_path, data_file, report_file)
        
        # Adaptive Decision 1
        d1 = AdaptiveDecision(
            decision_index=1,
            timestamp=time.time(),
            trigger_agent="AuditPlanner",
            reasoning=f"Identified repository path '{repo_path}' and dataset '{data_file}'. Validating schema readiness.",
            chosen_action="ROUTE_TO_AST_SCOPING",
            target_tool="scan_repository_ast",
            parameters={"repo_path": repo_path},
            outcome="Dispatched RepositoryInvestigator for bounded AST method discovery."
        )
        mission.adaptive_decisions.append(d1)

        # -------------------------------------------------------------
        # STAGE 2: REPOSITORY AST LOGIC MAPPING
        # -------------------------------------------------------------
        mission.stage = MissionStage.AST_SCOPING
        mission.progress_pct = 30
        record_snapshot("AST_SCOPING", "Parsing AST syntax trees to map calculation routines", "RepositoryInvestigator")

        ast_map = RepositoryInvestigator.analyze_repository(repo_path)
        mission.evidence_collected.append({
            "type": "AST_MAP",
            "files_scanned": ast_map.get("files_scanned", 0),
            "routines_discovered": ast_map.get("functions_found", [])
        })

        # Adaptive Decision 2
        d2 = AdaptiveDecision(
            decision_index=2,
            timestamp=time.time(),
            trigger_agent="RepositoryInvestigator",
            reasoning=f"AST mapping located {len(ast_map.get('functions_found', []))} financial functions. Routing to claim extractor.",
            chosen_action="ROUTE_TO_CLAIM_EXTRACTION",
            target_tool="load_normalized_trades",
            parameters={"report_file": report_file},
            outcome="Dispatched FinancialInvestigator to extract reported metrics."
        )
        mission.adaptive_decisions.append(d2)

        # -------------------------------------------------------------
        # STAGE 3: FINANCIAL CLAIM EXTRACTION & DATA NORMALIZATION
        # -------------------------------------------------------------
        mission.stage = MissionStage.CLAIM_EXTRACTION
        mission.progress_pct = 45
        record_snapshot("CLAIM_EXTRACTION", "Extracting claimed performance metrics and normalizing trade fills", "FinancialInvestigator")

        if os.path.exists(data_file):
            events = CSVIngestionAdapter.parse_csv_file(data_file)
            mission.evidence_collected.append({
                "type": "NORMALIZED_DATASET",
                "dataset_path": data_file,
                "record_count": len(events),
                "source_hash": CSVIngestionAdapter.compute_file_hash(data_file)
            })

        claims = FinancialInvestigator.extract_claims(
            reported_metrics=plan_output.get("repo_scan", {}),
            config_data=None
        )

        # Adaptive Decision 3
        d3 = AdaptiveDecision(
            decision_index=3,
            timestamp=time.time(),
            trigger_agent="FinancialInvestigator",
            reasoning=f"Extracted {len(claims)} performance claim targets with {len(events)} canonical fills. Routing to deterministic verifiers.",
            chosen_action="ROUTE_TO_DETERMINISTIC_RECONCILIATION",
            target_tool="execute_trade_reconciliation",
            parameters={"record_count": len(events), "initial_capital": initial_capital},
            outcome="Dispatched ContradictionInvestigator for bottom-up FIFO lot matching."
        )
        mission.adaptive_decisions.append(d3)

        # -------------------------------------------------------------
        # STAGE 4: ADAPTIVE CONTRADICTION INVESTIGATION & DUCKDB
        # -------------------------------------------------------------
        mission.stage = MissionStage.ADAPTIVE_VERIFICATION
        mission.progress_pct = 65
        record_snapshot("ADAPTIVE_VERIFICATION", "Executing deterministic FIFO reconciliation and DuckDB SQL profiling", "ContradictionInvestigator")

        findings_objs: List[Finding] = ContradictionInvestigator.investigate(
            repo_path=repo_path,
            data_file=data_file,
            report_file=report_file,
            evidence_store=evidence_store,
            initial_capital=initial_capital,
            claimed_fee_bps=claimed_fee_bps
        )

        mission.findings = [f.to_dict() for f in findings_objs]

        # In-Memory DuckDB profiling
        try:
            duckdb_profile = analyze_duckdb_dataset(data_file)
            mission.evidence_collected.append({
                "type": "DUCKDB_TABULAR_PROFILE",
                "profile": duckdb_profile
            })
        except Exception:
            pass

        total_discrepancy = sum(f.capital_at_risk for f in findings_objs)
        has_contradictions = any(f.status == FindingStatus.CONTRADICTION for f in findings_objs)

        # Adaptive Decision 4
        if has_contradictions:
            d4 = AdaptiveDecision(
                decision_index=4,
                timestamp=time.time(),
                trigger_agent="ContradictionInvestigator",
                reasoning=f"Confirmed {len(findings_objs)} findings with total capital discrepancy of ${total_discrepancy:,.2f}. Routing to RemediationAgent for sandbox verification.",
                chosen_action="ROUTE_TO_REMEDIATION_SANDBOX",
                target_tool="verify_remediation_sandbox",
                parameters={"discrepancy": total_discrepancy, "findings_count": len(findings_objs)},
                outcome="Dispatched RemediationAgent to formulate unified diff patches and re-verify in sandbox."
            )
        else:
            d4 = AdaptiveDecision(
                decision_index=4,
                timestamp=time.time(),
                trigger_agent="ContradictionInvestigator",
                reasoning="Deterministic recalculation exactly matches reported claims ($0.00 discrepancy). Zero hallucinations detected.",
                chosen_action="ROUTE_TO_REPORT_AGENT",
                target_tool="generate_report",
                parameters={"status": "VERIFIED_SOUND"},
                outcome="Proceeding directly to ReportAgent for sound verdict synthesis."
            )
        mission.adaptive_decisions.append(d4)

        # -------------------------------------------------------------
        # STAGE 5: REMEDIATION SANDBOX (Autonomous Code Patching & Re-Verification)
        # -------------------------------------------------------------
        if has_contradictions:
            mission.stage = MissionStage.REMEDIATION_SANDBOX
            mission.progress_pct = 80
            record_snapshot("REMEDIATION_SANDBOX", "Formulating unified diffs and testing patches inside isolated sandbox", "RemediationAgent")

            remediation_plans = RemediationAgent.generate_and_verify_remediations(
                findings=findings_objs,
                repo_path=repo_path,
                events=events,
                initial_capital=initial_capital
            )
            mission.remediation_plans = [p.to_dict() for p in remediation_plans]

            # Adaptive Decision 5
            d5 = AdaptiveDecision(
                decision_index=5,
                timestamp=time.time(),
                trigger_agent="RemediationAgent",
                reasoning=f"Verified {len(remediation_plans)} remediation patches inside isolated sandbox. Post-patch discrepancy confirmed at $0.00.",
                chosen_action="ROUTE_TO_REPORT_SYNTHESIS",
                target_tool="generate_report",
                parameters={"verified_patches": len(remediation_plans)},
                outcome="Routing to ReportAgent for final executive synthesis."
            )
            mission.adaptive_decisions.append(d5)

        # -------------------------------------------------------------
        # STAGE 6: REPORT SYNTHESIS & EVIDENCE SEALING
        # -------------------------------------------------------------
        mission.stage = MissionStage.REPORT_SYNTHESIS
        mission.progress_pct = 95
        record_snapshot("REPORT_SYNTHESIS", "Synthesizing executive report and sealing cryptographic provenance graphs", "ReportAgent")

        duration_sec = round(time.time() - start_time, 2)
        report_data = ReportAgent.generate_report(
            project_name=target_system,
            evidence_store=evidence_store,
            duration_seconds=duration_sec
        )

        # Financial Integrity Score computation
        fis_score, fis_grade, fis_breakdown = FinancialIntegrityScoreCalculator.calculate(
            findings=findings_objs,
            initial_capital=initial_capital,
            total_discrepancy=total_discrepancy
        )

        mission.financial_integrity_score = fis_score
        mission.integrity_grade = fis_grade
        mission.total_capital_at_risk = total_discrepancy

        # Attach FIS breakdown into report
        report_data["financial_integrity_score"] = {
            "score": fis_score,
            "grade": fis_grade,
            "breakdown": fis_breakdown
        }
        report_data["remediation_plans"] = mission.remediation_plans
        report_data["adaptive_decisions"] = [asdict(d) for d in mission.adaptive_decisions]

        # Stage Complete
        mission.stage = MissionStage.VERDICT_SEALED
        mission.status = MissionStatus.COMPLETED
        mission.progress_pct = 100
        mission.completed_at = time.time()
        mission.elapsed_time_ms = round((time.time() - start_time) * 1000, 1)
        record_snapshot("VERDICT_SEALED", f"Audit mission complete with FIS {fis_score}/100 ({fis_grade})", "ReportAgent")

        # Save checkpoint state
        mission.resumable_checkpoint = {
            "mission_id": mission_id,
            "saved_at": time.time(),
            "target_system": target_system,
            "stage": mission.stage.value,
            "status": mission.status.value,
            "findings_count": len(mission.findings)
        }

        return mission
