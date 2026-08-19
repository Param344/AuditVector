"""Statistical verification helpers."""

import math
from typing import List, Dict, Any


class FinancialStatistics:
    VERSION = "statistics_v1.0"

    @classmethod
    def calculate_win_rate(cls, trade_pnls: List[float]) -> Dict[str, Any]:
        if not trade_pnls:
            return {"win_rate": 0.0, "total_trades": 0, "winning_trades": 0, "losing_trades": 0}

        winning = [p for p in trade_pnls if p > 0]
        losing = [p for p in trade_pnls if p < 0]
        win_rate = (len(winning) / len(trade_pnls)) * 100.0

        return {
            "win_rate": round(win_rate, 2),
            "total_trades": len(trade_pnls),
            "winning_trades": len(winning),
            "losing_trades": len(losing),
            "avg_win": round(sum(winning) / len(winning), 2) if winning else 0.0,
            "avg_loss": round(sum(losing) / len(losing), 2) if losing else 0.0,
        }
