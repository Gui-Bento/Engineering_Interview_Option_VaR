import pandas as pd
import numpy as np


def filter_historical_data(file_path: str) -> pd.DataFrame:
    # Load the data

    historical_data = pd.read_csv(file_path)

    # Rename columns to easily access them
    historical_data.columns = ['Date', 'Portfolio', 'MarketRate_ccy1', 'MarketRate_ccy2', '1dShift_ccy1', '1dShift_ccy2',
                               'PnlVector_ccy1', 'PnlVector_ccy2', 'TotalPnl']

    # Skip the first row which may have an extra header, then reset index
    historical_data = historical_data[1:]
    historical_data.reset_index(drop=True, inplace=True)

    # Convert the Pnl Vector columns to numeric, handling commas as decimal points
    historical_data['PnlVector_ccy1'] = pd.to_numeric(historical_data['PnlVector_ccy1'].str.replace(',', '.'), errors='coerce')
    historical_data['PnlVector_ccy2'] = pd.to_numeric(historical_data['PnlVector_ccy2'].str.replace(',', '.'), errors='coerce')

    # Drop any rows with NaN values in the Pnl Vector columns
    returns_ccy1 = historical_data['PnlVector_ccy1'].dropna()
    returns_ccy2 = historical_data['PnlVector_ccy2'].dropna()

    historical_data['Return_A'] = returns_ccy1
    historical_data['Return_B'] = returns_ccy2

    return historical_data

def calculate_var(historical_data: pd.DataFrame) -> np.float64:
    # Parameters
    sensitivity = 1
    horizon = 1  # Horizon in days
    portfolio_value_a = 153084.81  # Current value for Currency A
    portfolio_value_b = 95891.51  # Current value for Currency B

    # Calculate daily returns for both currencies
    # Drop NaN values
    returns = historical_data[['Return_A', 'Return_B']].dropna()

    # Calculate scenario PnL for both currencies
    x = historical_data['PnlVector_ccy1'].iloc[-1]  # Latest rate for Currency A
    y = historical_data['PnlVector_ccy2'].iloc[-1]  # Latest rate for Currency B

    # FX Scenario PNL calculation
    fx_scenario_pnl_a = sensitivity * (np.exp(np.log(x / y) * np.sqrt(horizon)) - 1)
    fx_scenario_pnl_b = sensitivity * (np.exp(np.log(y / x) * np.sqrt(horizon)) - 1)

    # Print FX Scenario PNL for both currencies
    print(f"FX Scenario PNL for Currency A: {fx_scenario_pnl_a:.2f}")
    print(f"FX Scenario PNL for Currency B: {fx_scenario_pnl_b:.2f}")

    # PnLi calculation (using daily returns)
    delta_x_a = returns['Return_A'].iloc[-1] * portfolio_value_a
    delta_x_b = returns['Return_B'].iloc[-1] * portfolio_value_b

    pnl_i_a = sensitivity * delta_x_a
    pnl_i_b = sensitivity * delta_x_b

    # Print PnLi for both currencies
    print(f"PnLi for Currency A: {pnl_i_a:.2f}")
    print(f"PnLi for Currency B: {pnl_i_b:.2f}")

    # Calculate the historical PnLs (for weighted calculation)
    historical_pnl_a = returns['Return_A'] * portfolio_value_a
    historical_pnl_b = returns['Return_B'] * portfolio_value_b

    # Combine the PnLs and get the two worst ones
    all_pnls = np.concatenate((historical_pnl_a.values, historical_pnl_b.values))
    sorted_pnls = np.sort(all_pnls)

    # Get second and third worst PnL
    second_worst_pnl = sorted_pnls[1]  # Second worst
    third_worst_pnl = sorted_pnls[2]  # Third worst

    # Calculate the weighted PnL
    weighted_pnl = 0.4 * second_worst_pnl + 0.6 * third_worst_pnl


    return weighted_pnl

if __name__ == '__main__':
    file_path = 'historical_data.csv'
    historical_data = filter_historical_data(file_path)
    weighted_pnl = calculate_var(historical_data)
    # Print the weighted PnL
    print(f"Weighted PnL: {weighted_pnl:.2f}")