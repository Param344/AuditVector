"""IntegrityLab Synthetic System: Alpha Strategy Engine."""

import math

def calculate_portfolio_return(starting_capital: float, ending_capital: float) -> float:
    """Calculates overall strategy percentage return.
    
    BUG #1 (Return Polarity Contradiction): 
    The developer inverted the subtraction order when capital decreased,
    turning a loss into a positive return in the summary dashboard!
    """
    if ending_capital < starting_capital:
        # BUG: Subtraction inverted! (starting - ending instead of ending - starting)
        loss_gain = starting_capital - ending_capital
        return (loss_gain / starting_capital) * 100.0
    return ((ending_capital - starting_capital) / starting_capital) * 100.0


def calculate_reported_pnl(gross_profit: float, gross_loss: float) -> float:
    """Calculates total net realized PnL.
    
    BUG #4 (PnL Reconciliation Discrepancy):
    Adds gross loss instead of subtracting, creating an artificial surplus.
    """
    # BUG: Adding loss instead of subtracting
    return gross_profit + gross_loss
