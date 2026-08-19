"""Financial Investigator Agent for AuditVector."""

from typing import Dict, Any, List, Optional
from ..models.financial_event import FinancialEvent


class FinancialClaim:
    def __init__(self, claim_type: str, reported_value: Any, source: str, unit: str = "USD"):
        self.claim_type = claim_type
        self.reported_value = reported_value
        self.source = source
        self.unit = unit

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_type": self.claim_type,
            "reported_value": self.reported_value,
            "source": self.source,
            "unit": self.unit
        }


class FinancialInvestigator:
    """Agent 3: Extracts reported claims and prepares verification targets."""

    @classmethod
    def extract_claims(cls, reported_metrics: Dict[str, Any], config_data: Optional[Dict[str, Any]] = None) -> List[FinancialClaim]:
        claims: List[FinancialClaim] = []

        if "reported_pnl" in reported_metrics or "pnl" in reported_metrics:
            val = reported_metrics.get("reported_pnl", reported_metrics.get("pnl"))
            claims.append(FinancialClaim("REALIZED_PNL", val, reported_metrics.get("file_path", "report"), "USD"))

        if "reported_return_pct" in reported_metrics or "return_pct" in reported_metrics:
            val = reported_metrics.get("reported_return_pct", reported_metrics.get("return_pct"))
            claims.append(FinancialClaim("RETURN_PERCENTAGE", val, reported_metrics.get("file_path", "report"), "%"))

        if "reported_fees" in reported_metrics or "fees" in reported_metrics:
            val = reported_metrics.get("reported_fees", reported_metrics.get("fees"))
            claims.append(FinancialClaim("TOTAL_FEES", val, reported_metrics.get("file_path", "report"), "USD"))

        if config_data and "model_assumptions" in config_data:
            fee_bps = config_data["model_assumptions"].get("fee_model_bps")
            if fee_bps is not None:
                claims.append(FinancialClaim("CONFIGURED_FEE_BPS", fee_bps, "config.json", "bps"))

        return claims
