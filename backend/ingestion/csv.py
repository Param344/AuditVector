"""CSV Ingestion Adapter for AuditVector."""

import csv
import io
import hashlib
from typing import List, Dict, Any, Tuple
from ..models.financial_event import FinancialEvent
from .normalizer import IngestionNormalizer


class CSVIngestionAdapter:
    """Reads CSV trade/event datasets and converts to Canonical FinancialEvents."""

    @classmethod
    def load_from_file(cls, file_path: str) -> Tuple[List[FinancialEvent], str, int]:
        """Reads a CSV file, computes its SHA-256 hash, and returns normalized events."""
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        events = cls.load_from_string(content, source=file_path)
        return events, file_hash, len(events)

    @classmethod
    def load_from_string(cls, csv_text: str, source: str = "") -> List[FinancialEvent]:
        reader = csv.DictReader(io.StringIO(csv_text))
        events: List[FinancialEvent] = []
        for row in reader:
            if not any(row.values()):
                continue
            event = IngestionNormalizer.normalize_row(row, source=source)
            events.append(event)
        return events
