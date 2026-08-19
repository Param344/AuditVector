"""IntegrityLab Synthetic System: Clean Control Strategy (Case #5)."""

def calculate_clean_pnl(realized_trades: list) -> dict:
    """Correct, canonical financial calculation with no planted bugs."""
    total_realized_pnl = 0.0
    total_fees = 0.0
    
    for trade in realized_trades:
        # Proper net PnL: price diff * qty - fee
        trade_pnl = (trade['exit_price'] - trade['entry_price']) * trade['quantity']
        total_realized_pnl += trade_pnl
        total_fees += trade.get('fee', 0.0)
        
    net_profit = total_realized_pnl - total_fees
    return {
        "gross_pnl": total_realized_pnl,
        "total_fees": total_fees,
        "net_pnl": net_profit,
        "status": "VALID"
    }
