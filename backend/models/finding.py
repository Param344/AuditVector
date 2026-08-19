"""Finding, Evidence Contract, and Provenance Models for AuditVector."""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, Dict, Any, List
import datetime
import hashlib
import json


class FindingStatus(str, Enum):
    VERIFIED = "VERIFIED"
    CONTRADICTION = "CONTRADICTION"
    WARNING = "WARNING"
    UNVERIFIABLE = "UNVERIFIABLE"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class SourceCitation:
    file: str
    line_range: str
    source_hash: str = ""
    code_snippet: Optional[str] = None


@dataclass
class DataEvidence:
    dataset_id: str
    record_count: int
    source_path: str
    source_hash: str = ""


@dataclass
class ProvenanceMetadata:
    timestamp: str
    normalizer_version: str
    verifier_version: str
    transformation: str


@dataclass
class CalculationVariance:
    reported_pnl: Optional[float] = None
    reconstructed_pnl: Optional[float] = None
    reported_return_pct: Optional[float] = None
    reconstructed_return_pct: Optional[float] = None
    reported_fee: Optional[float] = None
    recalculated_fee: Optional[float] = None
    variance_amount: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Finding:
    """Evidence Contract compliant finding object."""
    finding_id: str
    title: str
    status: FindingStatus
    severity: Severity
    confidence: float
    claim: str
    sources: List[SourceCitation]
    data_evidence: Optional[DataEvidence]
    provenance: ProvenanceMetadata
    calculation: CalculationVariance
    verification_method: str
    verifier_name: str
    impact_level: str
    capital_at_risk: float = 0.0
    explanation: str = ""

    def validate_contract(self) -> bool:
        """Enforce: No Evidence Contract -> No Verified/Contradiction Finding."""
        if self.status in [FindingStatus.VERIFIED, FindingStatus.CONTRADICTION]:
            if not self.sources or not self.provenance or not self.verification_method:
                return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "title": self.title,
            "status": self.status.value,
            "severity": self.severity.value,
            "confidence": self.confidence,
            "claim": self.claim,
            "sources": [asdict(s) for s in self.sources],
            "data_evidence": asdict(self.data_evidence) if self.data_evidence else None,
            "provenance": asdict(self.provenance),
            "calculation": asdict(self.calculation),
            "verification": {
                "status": self.status.value,
                "method": self.verification_method,
                "verifier": self.verifier_name
            },
            "impact": {
                "level": self.impact_level,
                "capital_at_risk": self.capital_at_risk
            },
            "explanation": self.explanation
        }
