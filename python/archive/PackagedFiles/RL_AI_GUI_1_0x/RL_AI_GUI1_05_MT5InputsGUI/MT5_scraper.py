import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from indicators import indicator_functions
import json

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
    # Expecting start_date and end_date to be datetime objects
    rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
    if rates is None:
        print(f"Failed to get historical data for {symbol}")
        return None
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    return data

def calculate_indicators(data, symbol, timeframe, indicators, indicator_periods):
    for indicator in indicators:
        if indicator in indicator_functions:
            try:
                period = indicator_periods.get(indicator, None)
                data = indicator_functions[indicator](data, symbol, timeframe, period)
            except Exception as e:
                print(f"Error calculating {indicator}: {e}")
    return data

def scrape_mt5_data(symbol, timeframe, start_date, end_date, output_file, account, password, server, mt5_path, indicators, indicator_periods):
    if not initialize_mt5(mt5_path):
        return
    
    if not login_mt5(account, password, server):
        return

    print(f"Retrieving historical data for {symbol}...")
    data = get_historical_data(symbol, timeframe, start_date, end_date)
    if data is None:
        mt5.shutdown()
        return
    
    print("Calculating indicators...")
    data = calculate_indicators(data, symbol, timeframe, indicators, indicator_periods)
    
    print(f"Saving data to {output_file}...")
    data.to_csv(output_file, index=False)
    
    print("Data scraping completed successfully.")
    
    mt5.shutdown()

def load_indicator_settings():
    with open('indicator_settings.json', 'r') as f:
        settings = json.load(f)
    return settings

def load_account_settings():
    with open('account_settings.json', 'r') as f:
        settings = json.load(f)
    return settings

if __name__ == "__main__":
    settings = load_indicator_settings()
    account_settings = load_account_settings()

    symbol = settings['symbol']
    timeframe = settings['timeframe']
    start_date = datetime.strptime(settings['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(settings['end_date'], '%Y-%m-%d')
    indicator_periods = settings['indicator_periods']
    output_file = 'output.csv'  # Define your output file path

    account = account_settings['account']
    password = account_settings['password']
    server = account_settings['server']
    mt5_path = account_settings['mt5_path']
    indicators = list(indicator_periods.keys())

    scrape_mt5_data(symbol, timeframe, start_date, end_date, output_file, account, password, server, mt5_path, indicators, indicator_periods)