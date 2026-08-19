"""Evidence Store for validated Finding objects."""

from typing import List, Dict, Optional, Any
import json
from ..models.finding import Finding, FindingStatus


class EvidenceStore:
    """Stores findings, enforcing the Evidence Contract validation before acceptance."""

    def __init__(self):
        self._findings: Dict[str, Finding] = {}

    def add_finding(self, finding: Finding) -> bool:
        if not finding.validate_contract():
            raise ValueError(f"Finding {finding.finding_id} failed Evidence Contract validation.")
        self._findings[finding.finding_id] = finding
        return True

    def get_all(self) -> List[Finding]:
        return list(self._findings.values())

    def get_by_status(self, status: FindingStatus) -> List[Finding]:
        return [f for f in self._findings.values() if f.status == status]

    def to_json_dict(self) -> Dict[str, Any]:
        return {
            "total_findings": len(self._findings),
            "findings": [f.to_dict() for f in self._findings.values()]
        }
