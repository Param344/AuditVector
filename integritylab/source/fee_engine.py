"""IntegrityLab Synthetic System: Fee Engine."""

class FeeManager:
    # BUG #3 (Configuration Mismatch):
    # Hardcoded to 15 bps (0.0015) in runtime logic, while system config file claims 5 bps (0.0005)!
    RUNTIME_FEE_RATE = 0.0015  # 15 bps

    @classmethod
    def calculate_trade_fee(cls, notional: float) -> float:
        return notional * cls.RUNTIME_FEE_RATE

    @classmethod
    def calculate_ending_equity(cls, initial_equity: float, trade_pnl_net_of_fee: float, total_deducted_fees: float) -> float:
        """Calculates final account equity.
        
        BUG #2 (Fee Double-Counting):
        trade_pnl_net_of_fee already had trade fees deducted at the trade level.
        Deducting total_deducted_fees again double-counts fees!
        """
        # BUG: total_deducted_fees is subtracted a second time!
        return initial_equity + trade_pnl_net_of_fee - total_deducted_fees
