"""Remediation and Sandbox Verification Models for AuditVector."""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, Dict, Any, List


class PatchStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED_SOUND = "VERIFIED_SOUND"
    REGRESSION_FAILED = "REGRESSION_FAILED"
    APPLIED = "APPLIED"
    REJECTED = "REJECTED"


@dataclass
class SandboxVerificationMetrics:
    pre_patch_discrepancy: float
    post_patch_discrepancy: float
    discrepancy_resolved: bool
    pre_patch_status: str
    post_patch_status: str
    tests_passed: int
    tests_total: int
    execution_time_ms: float
    sandbox_path: str = "in_memory_sandbox"


@dataclass
class RemediationPlan:
    """Represents an autonomous code remediation plan with sandbox verification."""
    plan_id: str
    finding_id: str
    target_file: str
    line_range: str
    issue_type: str
    explanation: str
    original_code: str
    patched_code: str
    unified_diff: str
    status: PatchStatus = PatchStatus.PENDING
    verification_metrics: Optional[SandboxVerificationMetrics] = None
    human_approval_required: bool = True
    applied_to_repo: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "finding_id": self.finding_id,
            "target_file": self.target_file,
            "line_range": self.line_range,
            "issue_type": self.issue_type,
            "explanation": self.explanation,
            "original_code": self.original_code,
            "patched_code": self.patched_code,
            "unified_diff": self.unified_diff,
            "status": self.status.value,
            "verification_metrics": asdict(self.verification_metrics) if self.verification_metrics else None,
            "human_approval_required": self.human_approval_required,
            "applied_to_repo": self.applied_to_repo
        }
