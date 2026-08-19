"""Repository Scanner & File Hasher for AuditVector."""

import os
import hashlib
from typing import Dict, List, Any


class RepositoryScanner:
    """Scans code files and produces hashes, line counts, and candidate financial code paths."""

    FINANCIAL_KEYWORDS = [
        "pnl", "profit", "loss", "fee", "commission", "return", "drawdown",
        "sharpe", "position", "trade", "execution", "balance", "equity", "slippage"
    ]

    @classmethod
    def scan_directory(cls, dir_path: str, max_file_size_bytes: int = 1_000_000) -> Dict[str, Any]:
        results: Dict[str, Any] = {
            "total_files": 0,
            "financial_modules": [],
            "files": {}
        }

        for root, dirs, files in os.walk(dir_path):
            # Ignore git, cache, venv
            dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", ".venv", "node_modules", "dist"]]
            for file in files:
                if not file.endswith((".py", ".json", ".csv", ".yaml", ".yml", ".ts", ".js")):
                    continue

                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, dir_path)
                try:
                    size = os.path.getsize(abs_path)
                    if size > max_file_size_bytes:
                        continue

                    with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()

                    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                    line_count = len(content.splitlines())

                    # Check financial relevance
                    content_lower = content.lower()
                    relevance_hits = [k for k in cls.FINANCIAL_KEYWORDS if k in content_lower]

                    file_meta = {
                        "path": rel_path,
                        "abs_path": abs_path,
                        "hash": file_hash,
                        "line_count": line_count,
                        "keywords": relevance_hits,
                        "is_financial": len(relevance_hits) > 0
                    }

                    results["files"][rel_path] = file_meta
                    results["total_files"] += 1

                    if file_meta["is_financial"]:
                        results["financial_modules"].append(rel_path)

                except Exception as e:
                    continue

        return results
