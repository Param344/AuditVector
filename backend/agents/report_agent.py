"""Report Agent for AuditVector."""

import json
from typing import Dict, Any, List
from ..models.finding import Finding, FindingStatus, Severity
from ..evidence.evidence_store import EvidenceStore


class ReportAgent:
    """Compiles verified findings and evidence contracts into an Executive Audit Report."""

    @classmethod
    def generate_report(cls, project_name: str, evidence_store: EvidenceStore, duration_seconds: float = 12.4) -> Dict[str, Any]:
        findings = evidence_store.get_all()
        
        critical_count = sum(1 for f in findings if f.severity == Severity.CRITICAL)
        high_count = sum(1 for f in findings if f.severity == Severity.HIGH)
        medium_count = sum(1 for f in findings if f.severity == Severity.MEDIUM)
        low_count = sum(1 for f in findings if f.severity == Severity.LOW or f.status == FindingStatus.VERIFIED)

        contradictions = [f for f in findings if f.status == FindingStatus.CONTRADICTION]
        total_risk_capital = sum(f.capital_at_risk for f in contradictions)

        if critical_count > 0 or high_count > 0:
            verdict = "⚠️ RESULTS NOT FULLY TRUSTWORTHY"
            verdict_summary = "AuditVector identified verified integrity failures where the software's reported results contradict underlying transactional evidence."
        elif findings and all(f.status == FindingStatus.VERIFIED for f in findings):
            verdict = "✅ FINANCIAL INTEGRITY VERIFIED"
            verdict_summary = "All reported financial claims independently recomputed and proven consistent with underlying evidence."
        else:
            verdict = "⚠️ AUDIT INCONCLUSIVE / WARNINGS IDENTIFIED"
            verdict_summary = "Certain calculation claims could not be fully reconciled or require manual data inspection."

        report = {
            "title": "AUDITVECTOR FINANCIAL INTEGRITY REPORT",
            "project_name": project_name,
            "duration_seconds": duration_seconds,
            "verdict": verdict,
            "verdict_summary": verdict_summary,
            "summary_counts": {
                "total_findings": len(findings),
                "critical": critical_count,
                "high": high_count,
                "medium": medium_count,
                "low": low_count
            },
            "total_capital_discrepancy": total_risk_capital,
            "financial_impact": {
                "total_capital_discrepancy": total_risk_capital
            },
            "findings": [f.to_dict() for f in findings],
            "recommendations": [
                "Freeze live trading deployments relying on affected performance calculation routines.",
                "Review code logic in identified source locations adhering to the cited line ranges.",
                "Verify trade-level fee deduction pipelines against configuration assumptions."
            ]
        }

        return report

    @classmethod
    def render_markdown(cls, report_dict: Dict[str, Any]) -> str:
        md = []
        md.append(f"# {report_dict['title']}")
        md.append(f"**Project:** `{report_dict['project_name']}` | **Duration:** {report_dict['duration_seconds']}s\n")
        md.append(f"## Verdict: {report_dict['verdict']}")
        md.append(f"> {report_dict['verdict_summary']}\n")
        
        md.append("### Summary Counts")
        sc = report_dict["summary_counts"]
        md.append(f"* 🔴 **Critical:** {sc['critical']}")
        md.append(f"* 🟠 **High:** {sc['high']}")
        md.append(f"* 🟡 **Medium:** {sc['medium']}")
        md.append(f"* 🟢 **Low / Verified:** {sc['low']}\n")
        
        if report_dict["financial_impact"]["total_capital_discrepancy"] > 0:
            md.append(f"**Total Capital Discrepancy:** `${report_dict['financial_impact']['total_capital_discrepancy']:,.2f}`\n")

        md.append("## Findings & Evidence Chains")
        for f in report_dict["findings"]:
            md.append(f"### [{f['finding_id']}] {f['title']}")
            md.append(f"* **Status:** `{f['status']}` | **Severity:** `{f['severity']}` | **Confidence:** `{f['confidence']*100:.0f}%`")
            md.append(f"* **Claim:** {f['claim']}")
            md.append(f"* **Explanation:** {f['explanation']}")
            md.append(f"* **Verifier:** `{f['verification']['verifier']}` ({f['verification']['method']})")
            if f.get("sources"):
                md.append("* **Sources:** " + ", ".join([f"`{s['file']}:{s['line_range']}`" for s in f["sources"]]))
            md.append("")

        md.append("## Recommended Actions")
        for r in report_dict["recommendations"]:
            md.append(f"1. {r}")

        return "\n".join(md)
