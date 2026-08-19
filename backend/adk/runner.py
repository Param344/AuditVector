"""Google ADK Multi-Agent Orchestration Runner.

Orchestrates the 5-agent pipeline with Gemini model reasoning and deterministic tool bindings,
while providing an offline test mode for hermetic local execution.
"""

import time
import json
import logging
from typing import Dict, Any, List, Optional
from ..config.settings import settings
from ..evidence.evidence_store import EvidenceStore
from ..evidence.evidence_graph import EvidenceGraph
from ..models.finding import Finding
from .agents import FIVE_ADK_AGENTS
from .tools import (
    sanitize_text,
    scan_repository_ast,
    load_normalized_trades,
    execute_trade_reconciliation,
    analyze_duckdb_dataset,
    evaluate_metric_variance
)
from ..agents.audit_planner import AuditPlanner
from ..agents.repository_investigator import RepositoryInvestigator
from ..agents.financial_investigator import FinancialInvestigator
from ..agents.contradiction_investigator import ContradictionInvestigator
from ..agents.report_agent import ReportAgent

# Structured logger
logger = logging.getLogger("AuditVector.ADK")


class ADKSession:
    """Manages multi-agent execution session state and audit artifacts."""

    def __init__(self, audit_id: str, project_name: str):
        self.audit_id = audit_id
        self.project_name = project_name
        self.start_time = time.time()
        self.stage_logs: List[Dict[str, Any]] = []
        self.evidence_store = EvidenceStore()
        self.agent_outputs: Dict[str, Any] = {}

    def log_event(self, agent_name: str, stage: str, details: str, tool_name: Optional[str] = None):
        entry = {
            "timestamp": time.time(),
            "audit_id": self.audit_id,
            "agent_name": agent_name,
            "stage": stage,
            "tool_name": tool_name,
            "details": details
        }
        self.stage_logs.append(entry)


class ADKRunner:
    """Orchestrates the 5 Google ADK agents through the complete audit lifecycle."""

    @classmethod
    def run_audit(
        cls,
        audit_id: str,
        project_name: str,
        repo_path: str,
        data_file: str,
        report_file: str,
        initial_capital: float = 100_000.0,
        claimed_fee_bps: float = 5.0
    ) -> Dict[str, Any]:
        
        session = ADKSession(audit_id=audit_id, project_name=project_name)
        mode = "LIVE_GEMINI" if settings.is_gemini_configured() else "OFFLINE_DETERMINISTIC"

        # -------------------------------------------------------------
        # STEP 1: AUDIT PLANNER AGENT
        # -------------------------------------------------------------
        session.log_event("AuditPlanner", "PLANNING", "Formulating audit plan and scoping repository pathways")
        plan_output = AuditPlanner.plan_audit(repo_path, data_file, report_file)
        session.agent_outputs["planner"] = plan_output

        # -------------------------------------------------------------
        # STEP 2: REPOSITORY INVESTIGATOR AGENT (AST Logic Mapping)
        # -------------------------------------------------------------
        session.log_event("RepositoryInvestigator", "AST_ANALYSIS", "Mapping financial routines and AST call paths", tool_name="scan_repository_ast")
        ast_map = RepositoryInvestigator.analyze_repository(repo_path)
        session.agent_outputs["repository_investigator"] = ast_map

        # -------------------------------------------------------------
        # STEP 3: FINANCIAL INVESTIGATOR AGENT (Claim Extraction)
        # -------------------------------------------------------------
        session.log_event("FinancialInvestigator", "CLAIM_EXTRACTION", "Extracting reported metrics and config assumptions", tool_name="load_normalized_trades")
        claims = FinancialInvestigator.extract_claims(
            reported_metrics=plan_output.get("repo_scan", {}),
            config_data=None
        )
        session.agent_outputs["financial_investigator"] = [c.to_dict() for c in claims]

        # -------------------------------------------------------------
        # STEP 4: CONTRADICTION INVESTIGATOR AGENT (Deterministic Verifier Tools)
        # -------------------------------------------------------------
        session.log_event(
            "ContradictionInvestigator", 
            "RECONCILIATION", 
            "Executing deterministic trade reconciliation & variance evaluation",
            tool_name="execute_trade_reconciliation"
        )
        
        findings = ContradictionInvestigator.investigate(
            repo_path=repo_path,
            data_file=data_file,
            report_file=report_file,
            evidence_store=session.evidence_store,
            initial_capital=initial_capital,
            claimed_fee_bps=claimed_fee_bps
        )
        session.agent_outputs["contradiction_investigator"] = [f.to_dict() for f in findings]

        # Optional: Run DuckDB fast analytics for dataset validation
        session.log_event("ContradictionInvestigator", "DUCKDB_ANALYTICS", "Running analytical queries", tool_name="analyze_duckdb_dataset")
        try:
            duckdb_res = analyze_duckdb_dataset(data_file)
            session.agent_outputs["duckdb_profile"] = duckdb_res
        except Exception:
            pass

        # -------------------------------------------------------------
        # STEP 5: REPORT AGENT (Executive Synthesis)
        # -------------------------------------------------------------
        session.log_event("ReportAgent", "REPORT_GENERATION", "Synthesizing executive report from verified findings")
        duration = round(time.time() - session.start_time, 2)
        
        report_output = ReportAgent.generate_report(
            project_name=project_name,
            evidence_store=session.evidence_store,
            duration_seconds=duration
        )
        session.agent_outputs["report_agent"] = report_output

        # Generate Evidence Graphs
        graphs = [EvidenceGraph.build_graph(f) for f in findings]

        return {
            "status": "COMPLETED",
            "audit_id": audit_id,
            "project_name": project_name,
            "mode": mode,
            "gemini_model": settings.GEMINI_MODEL,
            "duration_seconds": duration,
            "agent_pipeline": {
                "planner": session.agent_outputs.get("planner"),
                "repository_investigator": session.agent_outputs.get("repository_investigator"),
                "financial_investigator": session.agent_outputs.get("financial_investigator"),
                "contradiction_investigator": session.agent_outputs.get("contradiction_investigator"),
                "report_agent": session.agent_outputs.get("report_agent")
            },
            "findings_count": len(findings),
            "report": report_output,
            "evidence_graphs": graphs,
            "execution_logs": session.stage_logs
        }
