"""Audit Worker orchestrating end-to-end execution via the Google ADK Runner."""

import uuid
from typing import Dict, Any, Optional
from ..adk.runner import ADKRunner


class AuditWorker:
    """Runs the asynchronous multi-agent audit workflow via ADKRunner."""

    @classmethod
    def execute_audit(
        cls,
        project_name: str,
        repo_path: str,
        data_file: str,
        report_file: str,
        initial_capital: float = 100_000.0,
        claimed_fee_bps: float = 5.0,
        audit_id: Optional[str] = None
    ) -> Dict[str, Any]:
        
        job_id = audit_id or f"audit-{uuid.uuid4().hex[:8]}"

        return ADKRunner.run_audit(
            audit_id=job_id,
            project_name=project_name,
            repo_path=repo_path,
            data_file=data_file,
            report_file=report_file,
            initial_capital=initial_capital,
            claimed_fee_bps=claimed_fee_bps
        )
