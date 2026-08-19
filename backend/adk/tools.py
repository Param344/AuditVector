"""Deterministic Tool Wrappers for Google ADK & Gemini Agents.

Rule: "AI reasons. Code proves. Evidence explains."
All numerical reconciliation, AST analysis, and PnL re-computations are executed
by deterministic Python modules, returning structured JSON results to the agent.
"""

from typing import Dict, Any, List, Optional
from ..verification.pnl_recalculator import PnLRecalculator
from ..verification.fee_recalculator import FeeRecalculator
from ..verification.return_calculator import ReturnCalculator
from ..verification.trade_reconciler import TradeReconciler
from ..verification.comparison import ComparisonEngine
from ..verification.duckdb_engine import DuckDBVerificationEngine
from ..ingestion.csv import CSVIngestionAdapter
from ..ingestion.reports import ReportIngestionAdapter
from ..ingestion.repository import RepositoryScanner
from ..security.secret_redactor import SecretRedactor


def sanitize_text(text: str) -> Dict[str, Any]:
    """Redacts secrets, API keys, tokens, and private keys from text before sending to LLM."""
    sanitized, count = SecretRedactor.sanitize(text)
    return {"sanitized_text": sanitized, "redactions_performed": count}


def scan_repository_ast(repo_path: str) -> Dict[str, Any]:
    """Scans repository code files and maps financial keywords and function definitions."""
    return RepositoryScanner.scan_directory(repo_path)


def load_normalized_trades(data_file_path: str) -> Dict[str, Any]:
    """Loads trade dataset and converts to canonical FinancialEvent representation."""
    events, file_hash, count = CSVIngestionAdapter.load_from_file(data_file_path)
    return {
        "event_count": count,
        "source_hash": file_hash,
        "events": [e.to_dict() for e in events]
    }


def execute_trade_reconciliation(
    data_file_path: str,
    report_file_path: str,
    initial_capital: float = 100_000.0,
    expected_fee_bps: float = 5.0
) -> Dict[str, Any]:
    """Executes bottom-up deterministic reconciliation of trades against reported summary."""
    events, file_hash, count = CSVIngestionAdapter.load_from_file(data_file_path)
    reported_metrics = ReportIngestionAdapter.parse_report_file(report_file_path)
    
    recon_result = TradeReconciler.reconcile(
        events=events,
        reported_metrics=reported_metrics,
        initial_capital=initial_capital,
        expected_fee_bps=expected_fee_bps
    )
    return recon_result


def analyze_duckdb_dataset(csv_path: str) -> Dict[str, Any]:
    """Runs high-performance analytical SQL query over raw trade data using DuckDB."""
    return DuckDBVerificationEngine.analyze_events_with_duckdb(csv_path)


def evaluate_metric_variance(
    metric_name: str,
    reported_val: Optional[float],
    reconstructed_val: Optional[float]
) -> Dict[str, Any]:
    """Evaluates mathematical variance against tolerances and assigns official FindingStatus."""
    return ComparisonEngine.evaluate_variance(metric_name, reported_val, reconstructed_val)


# Declarative tool registry for ADK function declarations
ADK_TOOL_REGISTRY = [
    sanitize_text,
    scan_repository_ast,
    load_normalized_trades,
    execute_trade_reconciliation,
    analyze_duckdb_dataset,
    evaluate_metric_variance
]
