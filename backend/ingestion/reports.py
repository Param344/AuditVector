"""Report & Performance Ingestion Adapter for AuditVector."""

import json
import csv
import hashlib
from typing import Dict, Any, Optional


class ReportIngestionAdapter:
    """Parses reported performance summaries (JSON or CSV) into structured metrics."""

    @classmethod
    def parse_report_file(cls, file_path: str) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        
        metrics: Dict[str, Any] = {"file_path": file_path, "file_hash": file_hash}
        
        if file_path.endswith(".json"):
            try:
                data = json.loads(content)
                metrics.update(data)
                # Unpack nested reported_metrics dictionary if present
                if "reported_metrics" in data and isinstance(data["reported_metrics"], dict):
                    metrics.update(data["reported_metrics"])
            except Exception as e:
                metrics["error"] = str(e)
        else:
            # Assume CSV
            lines = [l.strip() for l in content.splitlines() if l.strip()]
            for line in lines:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 2:
                    k, v = parts[0], parts[1]
                    try:
                        v_num = float(v.replace("%", "").replace("$", ""))
                        metrics[k] = v_num
                    except ValueError:
                        metrics[k] = v
        return metrics
