import strategies as s
import USER_CONFIG

# Risk parameters
starting_balance = USER_CONFIG.STARTING_BALANCE
stop_loss_percent_of_entry_price = USER_CONFIG.STOP_LOSS_PERCENT
leverage = USER_CONFIG.LEVERAGE
buying_power = USER_CONFIG.BUYING_POWER
contract_size = USER_CONFIG.CONTRACT_SIZE
total_fees_percent_per_trade = USER_CONFIG.FEE_PERCENT
risk_to_reward_ratio = USER_CONFIG.RR

# Contract multiplier
contract_multiplier = lambda: 50 if s.INSTRUMENT == "ES" else 1

def calculate_stop_loss(entry_price, position):
    if position == "long":
        return entry_price * (1 - stop_loss_percent_of_entry_price)
    else: 
        return entry_price * (1 + stop_loss_percent_of_entry_price)

def calculate_take_profit(entry_price, position):
    if position == "long":
        return entry_price * (1 + stop_loss_percent_of_entry_price * risk_to_reward_ratio)
    else:
        return entry_price * (1 - stop_loss_percent_of_entry_price * risk_to_reward_ratio)

# Linear future contract return
def calculate_return(entry_price, exit_price, position, contract_size):

    if position == "long":
        gross_profit = ((exit_price - entry_price) * contract_multiplier * contract_size)
    else:
        gross_profit = ((entry_price - exit_price) * contract_multiplier * contract_size)
    
    # Simple fee structure
    entry_fee = entry_price * contract_size * total_fees_percent_per_trade
    exit_fee = exit_price * contract_size * total_fees_percent_per_trade
    total_fees = entry_fee + exit_fee

    net_profit = gross_profit - total_fees
    return net_profit, total_fees