"""Official Google ADK Agent Definitions for AuditVector.

Uses the official google.adk.agents.Agent class to define the 5 specialized agents.
"""

from typing import Dict, Any, List, Optional
from google.adk.agents import Agent
from ..config.settings import settings
from .tools import (
    sanitize_text,
    scan_repository_ast,
    load_normalized_trades,
    execute_trade_reconciliation,
    analyze_duckdb_dataset,
    evaluate_metric_variance,
    ADK_TOOL_REGISTRY
)


# System instructions
AUDIT_PLANNER_PROMPT = """You are the AUDIT PLANNER AGENT for AuditVector.
Your goal is to inspect repository metadata, trade dataset paths, and report summaries to formulate a targeted, multi-step financial audit plan.
You do NOT perform financial arithmetic yourself. You define the investigation scope and prioritize calculation pathways for downstream agents."""

REPO_INVESTIGATOR_PROMPT = """You are the REPOSITORY INVESTIGATOR AGENT for AuditVector.
Your goal is to analyze source code ASTs, locate financial calculation functions (PnL, return, fee, inventory, balance), and extract candidate code evidence.
Do NOT read or send entire repositories. Focus on bounded AST nodes and function signatures.
You do NOT compute mathematical results."""

FINANCIAL_INVESTIGATOR_PROMPT = """You are the FINANCIAL INVESTIGATOR AGENT for AuditVector.
Your goal is to extract reported financial claims from performance reports, execution logs, and config files (e.g. reported PnL, return %, claimed fee bps).
Convert each claim into a structured verification target.
You must NOT calculate or invent replacement numbers."""

CONTRADICTION_INVESTIGATOR_PROMPT = """You are the CONTRADICTION INVESTIGATOR AGENT for AuditVector.
You are the primary integrity auditor.
CRITICAL MANDATE: AI reasons. Code proves. Evidence explains.
You MUST invoke deterministic tools (execute_trade_reconciliation, evaluate_metric_variance) to calculate true financial values.
Compare reported metrics against deterministic recalculation results.
Assign official statuses:
- VERIFIED: Independent deterministic calculation matches claim.
- CONTRADICTION: Reconstructed value conflicts with system claim (e.g., polarity reversal, PnL mismatch, fee double-counting).
- WARNING: Parameter deviation (e.g. config fee rate mismatch).
- UNVERIFIABLE: Missing underlying transactional fields.
Formulate Evidence Contracts for every verified finding."""

REPORT_AGENT_PROMPT = """You are the REPORT AGENT for AuditVector.
Your goal is to synthesize the verified evidence, finding classifications, capital-at-risk calculations, and provenance metadata into an Executive Financial Integrity Report.
You must NOT invent findings, alter statuses, or perform independent arithmetic.
Grounded truth comes exclusively from the deterministic Evidence Contracts."""


def build_five_adk_agents(model_name: Optional[str] = None) -> Dict[str, Agent]:
    """Instantiates and returns the 5 official google.adk.agents.Agent objects."""
    resolved_model = model_name or settings.get_resolved_model()

    planner = Agent(
        name="AuditPlanner",
        description="Audit Scope & Strategy Planner",
        instruction=AUDIT_PLANNER_PROMPT,
        model=resolved_model,
        tools=[scan_repository_ast, sanitize_text]
    )

    repository_investigator = Agent(
        name="RepositoryInvestigator",
        description="Codebase AST & Logic Pathway Mapper",
        instruction=REPO_INVESTIGATOR_PROMPT,
        model=resolved_model,
        tools=[scan_repository_ast, sanitize_text]
    )

    financial_investigator = Agent(
        name="FinancialInvestigator",
        description="Financial Claim & Target Extractor",
        instruction=FINANCIAL_INVESTIGATOR_PROMPT,
        model=resolved_model,
        tools=[load_normalized_trades, sanitize_text]
    )

    contradiction_investigator = Agent(
        name="ContradictionInvestigator",
        description="Deterministic Contradiction & Integrity Investigator",
        instruction=CONTRADICTION_INVESTIGATOR_PROMPT,
        model=resolved_model,
        tools=[execute_trade_reconciliation, evaluate_metric_variance, analyze_duckdb_dataset]
    )

    report_agent = Agent(
        name="ReportAgent",
        description="Executive Integrity Report Synthesizer",
        instruction=REPORT_AGENT_PROMPT,
        model=resolved_model,
        tools=[sanitize_text]
    )

    return {
        "planner": planner,
        "repository_investigator": repository_investigator,
        "financial_investigator": financial_investigator,
        "contradiction_investigator": contradiction_investigator,
        "report_agent": report_agent
    }


# Singleton registry of official ADK agents
FIVE_ADK_AGENTS = build_five_adk_agents()
