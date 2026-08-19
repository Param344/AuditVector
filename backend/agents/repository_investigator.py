"""Repository Investigator Agent for AuditVector."""

import ast
import os
import hashlib
from typing import Dict, Any, List, Optional


class FinancialCalculationMap:
    """Represents an AST-derived map of financial logic paths in a codebase."""

    def __init__(self):
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.call_graph: List[Dict[str, str]] = []

    def add_module(self, path: str, functions: List[str], financial_keywords: List[str], file_hash: str):
        self.modules[path] = {
            "functions": functions,
            "keywords": financial_keywords,
            "hash": file_hash
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_mapped_modules": len(self.modules),
            "modules": self.modules,
            "call_graph": self.call_graph
        }


class RepositoryInvestigator:
    """Agent 2: Analyzes Python ASTs to map financial calculation pathways."""

    FINANCIAL_TERMS = {
        "pnl": ["pnl", "profit", "loss", "net_profit", "gross_profit"],
        "fee": ["fee", "commission", "cost", "charge"],
        "return": ["return", "roi", "return_pct", "percentage_gain"],
        "position": ["position", "inventory", "exposure", "holding"],
        "trade": ["trade", "order", "fill", "execution"]
    }

    @classmethod
    def analyze_repository(cls, repo_path: str) -> Dict[str, Any]:
        calc_map = FinancialCalculationMap()
        
        for root, _, files in os.walk(repo_path):
            for file in files:
                if not file.endswith(".py"):
                    continue
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, repo_path)
                
                try:
                    with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                        source_code = f.read()

                    file_hash = hashlib.sha256(source_code.encode("utf-8")).hexdigest()
                    tree = ast.parse(source_code, filename=rel_path)

                    functions_found = []
                    keywords_found = set()

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            fn_name = node.name.lower()
                            functions_found.append(node.name)
                            for category, terms in cls.FINANCIAL_TERMS.items():
                                if any(term in fn_name for term in terms):
                                    keywords_found.add(category)

                    calc_map.add_module(
                        path=rel_path,
                        functions=functions_found,
                        financial_keywords=list(keywords_found),
                        file_hash=file_hash
                    )
                except Exception as e:
                    continue

        return calc_map.to_dict()
