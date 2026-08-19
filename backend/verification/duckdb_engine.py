"""DuckDB Analytical Verification Engine."""

import duckdb
from typing import Dict, Any, List, Optional
from ..models.financial_event import FinancialEvent


class DuckDBVerificationEngine:
    """Uses DuckDB for high-throughput deterministic queries over trade events."""
    VERSION = "duckdb_engine_v1.0"

    @classmethod
    def analyze_events_with_duckdb(cls, csv_path: str) -> Dict[str, Any]:
        """Runs fast in-memory SQL aggregation over raw trade CSV files."""
        con = duckdb.connect(database=":memory:")
        
        # Read CSV with duckdb auto-detection
        con.execute(f"CREATE TABLE trades AS SELECT * FROM read_csv_auto('{csv_path}')")
        
        # Summary metrics query
        summary = con.execute("""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT symbol) as unique_symbols
            FROM trades
        """).fetchone()

        total_records = summary[0] if summary else 0
        unique_symbols = summary[1] if summary else 0

        # Symbol breakdown query
        symbol_stats = con.execute("""
            SELECT 
                symbol,
                COUNT(*) as trade_count
            FROM trades
            GROUP BY symbol
            ORDER BY trade_count DESC
        """).fetchall()

        con.close()

        return {
            "total_records": total_records,
            "unique_symbols": unique_symbols,
            "symbol_stats": [{"symbol": s[0], "count": s[1]} for s in symbol_stats],
            "engine": "DuckDB In-Memory",
            "version": cls.VERSION
        }
