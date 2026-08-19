"""Comparison & Status Evaluator."""

from typing import Dict, Any, Optional
from ..models.finding import FindingStatus, Severity


class ComparisonEngine:
    """Evaluates numerical and semantic variances and maps to official FindingStatus."""
    VERSION = "comparison_engine_v1.0"

    @classmethod
    def evaluate_variance(
        cls,
        metric_name: str,
        reported_val: Optional[float],
        reconstructed_val: Optional[float],
        relative_tolerance: float = 0.01,
        absolute_tolerance: float = 1.0
    ) -> Dict[str, Any]:
        
        if reported_val is None or reconstructed_val is None:
            return {
                "status": FindingStatus.UNVERIFIABLE,
                "variance": None,
                "reason": f"Missing value for {metric_name} (reported={reported_val}, reconstructed={reconstructed_val})"
            }

        diff = reported_val - reconstructed_val
        abs_diff = abs(diff)

        # Check sign inversion for returns/PnL
        if (reported_val > 0 and reconstructed_val < -0.01) or (reported_val < 0 and reconstructed_val > 0.01):
            return {
                "status": FindingStatus.CONTRADICTION,
                "variance": diff,
                "abs_diff": abs_diff,
                "severity": Severity.CRITICAL,
                "reason": f"Polarity/Sign contradiction in {metric_name}: reported={reported_val}, reconstructed={reconstructed_val}"
            }

        # Check tolerance match
        denom = max(abs(reported_val), abs(reconstructed_val), 1.0)
        rel_diff = abs_diff / denom

        if abs_diff <= absolute_tolerance or rel_diff <= relative_tolerance:
            return {
                "status": FindingStatus.VERIFIED,
                "variance": diff,
                "abs_diff": abs_diff,
                "severity": Severity.LOW,
                "reason": f"Values match within tolerance ({rel_diff*100:.2f}% rel variance)"
            }

        # Material mismatch
        if rel_diff > 0.10:
            return {
                "status": FindingStatus.CONTRADICTION,
                "variance": diff,
                "abs_diff": abs_diff,
                "severity": Severity.HIGH if abs_diff > 500 else Severity.MEDIUM,
                "reason": f"Material discrepancy in {metric_name}: variance of {diff:.2f} ({rel_diff*100:.1f}%)"
            }
        else:
            return {
                "status": FindingStatus.WARNING,
                "variance": diff,
                "abs_diff": abs_diff,
                "severity": Severity.MEDIUM,
                "reason": f"Minor discrepancy in {metric_name} exceeding tolerance: variance of {diff:.2f}"
            }
