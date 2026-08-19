"""Evidence Graph Generator for trace links."""

from typing import Dict, Any, List
from ..models.finding import Finding


class EvidenceGraph:
    """Generates node-and-edge graph representations for UI visualization."""

    @classmethod
    def build_graph(cls, finding: Finding) -> Dict[str, Any]:
        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []

        # 1. Finding node
        f_node_id = f"finding_{finding.finding_id}"
        nodes.append({
            "id": f_node_id,
            "label": f"{finding.finding_id}: {finding.title}",
            "type": "finding",
            "status": finding.status.value,
            "severity": finding.severity.value
        })

        # 2. Source nodes
        for idx, src in enumerate(finding.sources):
            s_id = f"src_{idx}_{finding.finding_id}"
            nodes.append({
                "id": s_id,
                "label": f"{src.file}:{src.line_range}",
                "type": "source_code",
                "hash": src.source_hash[:8] if src.source_hash else ""
            })
            edges.append({"source": s_id, "target": f_node_id, "label": "cites"})

        # 3. Data evidence node
        if finding.data_evidence:
            d_id = f"data_{finding.finding_id}"
            nodes.append({
                "id": d_id,
                "label": f"{finding.data_evidence.dataset_id} ({finding.data_evidence.record_count} records)",
                "type": "trade_data",
                "path": finding.data_evidence.source_path
            })
            
            # Normalization node
            norm_id = f"norm_{finding.finding_id}"
            nodes.append({
                "id": norm_id,
                "label": f"Normalizer ({finding.provenance.normalizer_version})",
                "type": "normalization"
            })
            edges.append({"source": d_id, "target": norm_id, "label": "normalizes"})

            # Verification calculation node
            calc_id = f"calc_{finding.finding_id}"
            nodes.append({
                "id": calc_id,
                "label": f"Verifier: {finding.verifier_name}",
                "type": "verification_engine"
            })
            edges.append({"source": norm_id, "target": calc_id, "label": "calculates"})
            edges.append({"source": calc_id, "target": f_node_id, "label": "proves"})

        return {
            "finding_id": finding.finding_id,
            "nodes": nodes,
            "edges": edges
        }
