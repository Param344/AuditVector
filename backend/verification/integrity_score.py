"""Financial Integrity Score (FIS) Calculator for AuditVector.

Computes a deterministic 0-100 institutional confidence score based on
verified contradictions, capital-at-risk ratio, and severity classifications.
"""

from typing import List, Dict, Any, Tuple
from ..models.finding import Finding, Severity, FindingStatus


class FinancialIntegrityScoreCalculator:
    """Calculates deterministic Financial Integrity Score (0-100) and grade."""

    @classmethod
    def calculate(
        cls,
        findings: List[Finding],
        initial_capital: float = 100_000.0,
        total_discrepancy: float = 0.0
    ) -> Tuple[float, str, Dict[str, Any]]:
        
        # Only penalize findings that are CONTRADICTION or WARNING (never penalize VERIFIED sound findings)
        contradictions = [f for f in findings if f.status in [FindingStatus.CONTRADICTION, FindingStatus.WARNING]]

        if not contradictions and total_discrepancy == 0.0:
            return 100.0, "A+", {
                "critical_count": 0,
                "high_count": 0,
                "medium_count": 0,
                "low_count": 0,
                "deductions": {},
                "summary": "100% Deterministic Financial Integrity Verified (0 False Positives)"
            }

        score = 100.0
        deductions: Dict[str, float] = {}

        crit_count = sum(1 for f in contradictions if f.severity == Severity.CRITICAL)
        high_count = sum(1 for f in contradictions if f.severity == Severity.HIGH)
        med_count = sum(1 for f in contradictions if f.severity == Severity.MEDIUM)
        low_count = sum(1 for f in contradictions if f.severity in [Severity.LOW, Severity.INFO])

        # Severity penalties
        if crit_count > 0:
            crit_penalty = crit_count * 35.0
            score -= crit_penalty
            deductions["critical_contradictions"] = crit_penalty

        if high_count > 0:
            high_penalty = high_count * 18.0
            score -= high_penalty
            deductions["high_severity_flaws"] = high_penalty

        if med_count > 0:
            med_penalty = med_count * 8.0
            score -= med_penalty
            deductions["config_parameter_drift"] = med_penalty

        if low_count > 0:
            low_penalty = low_count * 2.0
            score -= low_penalty
            deductions["minor_deviations"] = low_penalty

        # Capital at risk ratio penalty
        if initial_capital > 0 and total_discrepancy > 0:
            ratio = total_discrepancy / initial_capital
            cap_penalty = min(25.0, round(ratio * 50.0, 1))
            score -= cap_penalty
            deductions["capital_at_risk_ratio"] = cap_penalty

        final_score = max(0.0, min(100.0, round(score, 1)))

        if final_score >= 90.0:
            grade = "A+"
        elif final_score >= 75.0:
            grade = "B"
        elif final_score >= 50.0:
            grade = "C"
        else:
            grade = "F"

        breakdown = {
            "critical_count": crit_count,
            "high_count": high_count,
            "medium_count": med_count,
            "low_count": low_count,
            "deductions": deductions,
            "total_discrepancy": total_discrepancy,
            "capital_ratio_pct": round((total_discrepancy / initial_capital) * 100, 2) if initial_capital > 0 else 0.0,
            "grade_description": (
                "Institutional Soundness Verified" if grade == "A+"
                else "Parameter Drift Detected" if grade == "B"
                else "Execution Slippage Drag" if grade == "C"
                else "Critical Integrity Failure Discovered"
            )
        }

        return final_score, grade, breakdown
