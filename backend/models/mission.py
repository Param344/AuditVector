"""Audit Mission Models for AuditVector.

Encapsulates mission goal, target system, scoped pathways, agent execution state,
evidence collection, integrity scores, and resumable checkpoints.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, Dict, Any, List
import time


class MissionStatus(str, Enum):
    INITIALIZED = "INITIALIZED"
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class MissionStage(str, Enum):
    PLANNING = "PLANNING"
    AST_SCOPING = "AST_SCOPING"
    CLAIM_EXTRACTION = "CLAIM_EXTRACTION"
    EVIDENCE_EVALUATION = "EVIDENCE_EVALUATION"
    ADAPTIVE_VERIFICATION = "ADAPTIVE_VERIFICATION"
    REMEDIATION_SANDBOX = "REMEDIATION_SANDBOX"
    REPORT_SYNTHESIS = "REPORT_SYNTHESIS"
    VERDICT_SEALED = "VERDICT_SEALED"


@dataclass
class MissionScope:
    repo_path: str
    data_file: str
    report_file: str
    claimed_fee_bps: float = 5.0
    initial_capital: float = 100_000.0


@dataclass
class AdaptiveDecision:
    decision_index: int
    timestamp: float
    trigger_agent: str
    reasoning: str
    chosen_action: str
    target_tool: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    outcome: str = ""


@dataclass
class AuditMission:
    """Master Audit Mission containing full lifecycle and evidence state."""
    mission_id: str
    goal: str
    target_system: str
    scope: MissionScope
    status: MissionStatus = MissionStatus.INITIALIZED
    stage: MissionStage = MissionStage.PLANNING
    progress_pct: int = 0
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    elapsed_time_ms: float = 0.0
    financial_integrity_score: float = 100.0
    integrity_grade: str = "A+"
    total_capital_at_risk: float = 0.0
    evidence_collected: List[Dict[str, Any]] = field(default_factory=list)
    findings: List[Dict[str, Any]] = field(default_factory=list)
    remediation_plans: List[Dict[str, Any]] = field(default_factory=list)
    adaptive_decisions: List[AdaptiveDecision] = field(default_factory=list)
    replay_snapshots: List[Dict[str, Any]] = field(default_factory=list)
    resumable_checkpoint: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "goal": self.goal,
            "target_system": self.target_system,
            "scope": asdict(self.scope),
            "status": self.status.value,
            "stage": self.stage.value,
            "progress_pct": self.progress_pct,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "elapsed_time_ms": self.elapsed_time_ms,
            "financial_integrity_score": self.financial_integrity_score,
            "integrity_grade": self.integrity_grade,
            "total_capital_at_risk": self.total_capital_at_risk,
            "evidence_collected": self.evidence_collected,
            "findings_count": len(self.findings),
            "findings": self.findings,
            "remediation_plans": self.remediation_plans,
            "adaptive_decisions": [asdict(d) for d in self.adaptive_decisions],
            "replay_snapshots": self.replay_snapshots,
            "resumable_checkpoint": self.resumable_checkpoint
        }
