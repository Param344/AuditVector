"""Remediation Agent for AuditVector.

Autonomously formulates minimal unified diff patches for confirmed contradictions,
verifies them inside the isolated sandbox, and establishes post-patch financial integrity.
"""

from typing import List, Dict, Any, Optional
from ..models.finding import Finding, FindingStatus
from ..models.remediation import RemediationPlan, PatchStatus
from ..models.financial_event import FinancialEvent
from ..remediation.patch_generator import PatchGenerator
from ..remediation.sandbox import RemediationSandbox


class RemediationAgent:
    """Remediation Agent responsible for formulating and sandboxing code patches."""
    AGENT_NAME = "RemediationAgent"

    @classmethod
    def generate_and_verify_remediations(
        cls,
        findings: List[Finding],
        repo_path: str,
        events: List[FinancialEvent],
        initial_capital: float = 100_000.0
    ) -> List[RemediationPlan]:
        
        plans: List[RemediationPlan] = []
        
        for finding in findings:
            if finding.status in [FindingStatus.CONTRADICTION, FindingStatus.WARNING]:
                plan = PatchGenerator.generate_patch_for_finding(finding, repo_path)
                if plan:
                    # Verify inside isolated sandbox immediately
                    verified_plan = RemediationSandbox.verify_patch(
                        plan=plan,
                        finding=finding,
                        events=events,
                        initial_capital=initial_capital
                    )
                    plans.append(verified_plan)

        return plans
