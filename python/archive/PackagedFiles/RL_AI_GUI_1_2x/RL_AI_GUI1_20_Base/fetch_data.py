import MetaTrader5 as mt5
import pandas as pd
import json
from datetime import datetime
from indicators.functions import initialize_indicators, get_available_indicators
# Initialize indicators
initialize_indicators()
from indicators import indicator_functions  # Ensure this import works

def initialize_mt5(mt5_path):
    if not mt5.initialize(mt5_path):
        print(f"Failed to initialize MT5 with path {mt5_path}")
        return False
    return True

def login_mt5(account, password, server):
    if not mt5.login(account, password=password, server=server):
        print(f"Failed to login to MT5 account {account} on server {server}")
        return False
    return True

def get_historical_data(symbol, timeframe, start_date, end_date):
    rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
    if rates is None:
        print(f"Failed to get historical data for {symbol}")
        return None
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    return data

def save_indicator_settings(symbol, timeframe, start_date, end_date, indicator_periods, output_file='indicator_settings.json'):
    settings = {
        'symbol': symbol,
        'timeframe': timeframe,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'indicator_periods': indicator_periods
    }
    with open(output_file, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f"Settings saved to {output_file}")

if __name__ == "__main__":
    # Example settings
    symbol = 'EURUSD'
    timeframe = mt5.TIMEFRAME_H1
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    indicator_periods = {
        'alligator': {'jaw': 13, 'teeth': 8, 'lips': 5, 'jaw_shift': 8, 'teeth_shift': 5, 'lips_shift': 3}
    }
    mt5_path = 'path_to_mt5_terminal'
    account = 'your_account_number'
    password = 'your_password'
    server = 'your_server'

    if initialize_mt5(mt5_path) and login_mt5(account, password, server):
        data = get_historical_data(symbol, timeframe, start_date, end_date)
        if data is not None:
            save_indicator_settings(symbol, timeframe, start_date, end_date, indicator_periods)
        mt5.shutdown()