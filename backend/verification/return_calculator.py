"""Deterministic Return & Polarity Inversion Detector."""

from typing import Dict, Any, Optional


class ReturnCalculator:
    """Calculates return percentages and detects return sign polarity contradiction bugs."""
    VERSION = "return_calculator_v1.0"

    @classmethod
    def calculate_return(
        cls, 
        initial_capital: float, 
        realized_pnl: float, 
        reported_return_pct: Optional[float] = None
    ) -> Dict[str, Any]:
        
        if initial_capital <= 0:
            return {
                "error": "Initial capital must be positive",
                "calculated_return_pct": 0.0,
                "polarity_contradiction": False
            }

        calculated_return_pct = (realized_pnl / initial_capital) * 100.0
        polarity_contradiction = False
        variance_pct = 0.0

        if reported_return_pct is not None:
            variance_pct = reported_return_pct - calculated_return_pct
            # Detect polarity sign contradiction: e.g. reported is positive while reconstructed is negative
            if (reported_return_pct > 0 and calculated_return_pct < -0.01) or \
               (reported_return_pct < 0 and calculated_return_pct > 0.01):
                # Also check if magnitude is identical or opposite
                polarity_contradiction = True

        return {
            "initial_capital": initial_capital,
            "realized_pnl": realized_pnl,
            "calculated_return_pct": round(calculated_return_pct, 4),
            "reported_return_pct": reported_return_pct,
            "variance_pct": round(variance_pct, 4),
            "polarity_contradiction": polarity_contradiction,
            "verifier_version": cls.VERSION
        }
