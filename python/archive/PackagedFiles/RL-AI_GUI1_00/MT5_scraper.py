import os
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd

def initialize_mt5(mt5_path):
    if not os.path.exists(mt5_path):
        print(f"MT5 terminal executable not found at {mt5_path}")
        return False
    
    print(f"MT5 terminal executable found at {mt5_path}")
    
    print("Attempting to initialize MT5...")
    if not mt5.initialize(path=mt5_path):
        print("Failed to initialize MT5")
        print(f"Error code: {mt5.last_error()}")
        return False
    
    return True

def login_mt5(account, password, server):
    print(f"Attempting to login with account: {account}, server: {server}")
    authorized = mt5.login(account, password, server)
    
    if not authorized:
        print(f"Failed to login to MT5 account {account}")
        print(f"Error code: {mt5.last_error()}")
        mt5.shutdown()
        return False
    
    print(f"Successfully logged in to MT5 account {account}")
    return True

def get_historical_data(symbol, timeframe, start_date, end_date):
    rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
    if rates is None:
        print(f"Failed to retrieve data for {symbol}")
        return None
    return pd.DataFrame(rates)

def calculate_indicators(data, symbol, timeframe):
    # Calculate Moving Average (example)
    ma = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data))
    data['MA'] = [rate['close'] for rate in ma]
    
    # Calculate RSI (example)
    rsi = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data))
    data['RSI'] = [rate['close'] for rate in rsi]
    
    # Calculate Alligator Indicator
    jaw_period = 13
    teeth_period = 8
    lips_period = 5
    jaw_shift = 8
    teeth_shift = 5
    lips_shift = 3
    
    jaw = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + jaw_shift)
    teeth = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + teeth_shift)
    lips = mt5.copy_rates_from_pos(symbol, timeframe, 0, len(data) + lips_shift)
    
    data['Alligator_Jaw'] = [rate['close'] for rate in jaw[jaw_shift:]]
    data['Alligator_Teeth'] = [rate['close'] for rate in teeth[teeth_shift:]]
    data['Alligator_Lips'] = [rate['close'] for rate in lips[lips_shift:]]
    
    return data

def scrape_mt5_data(symbol, timeframe, start_date, end_date, output_file):
    mt5_path = r'C:\Program Files\PlexyTrade MT5 Terminal\terminal64.exe'  # Replace with the actual path to your MT5 terminal
    
    if not initialize_mt5(mt5_path):
        return
    
    account = 3021640  # Replace with account number
    password = 'AItester1!'  # Replace with your password
    server = 'PlexyTrade-Server01'  # Replace with your server
    
    if not login_mt5(account, password, server):
        return

    print(f"Retrieving historical data for {symbol}...")
    data = get_historical_data(symbol, timeframe, start_date, end_date)
    if data is None:
        mt5.shutdown()
        return
    
    print("Calculating indicators...")
    data = calculate_indicators(data, symbol, timeframe)
    
    print(f"Saving data to {output_file}...")
    data.to_csv(output_file, index=False)
    
    print("Data scraping completed successfully.")
    
    mt5.shutdown()

# Example usage
if __name__ == "__main__":
    symbol = 'XAUUSD'
    timeframe = mt5.TIMEFRAME_H1
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    output_file = 'output.csv'
    
    scrape_mt5_data(symbol, timeframe, start_date, end_date, output_file)