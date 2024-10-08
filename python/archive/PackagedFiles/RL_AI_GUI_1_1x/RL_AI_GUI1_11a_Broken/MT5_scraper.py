import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from indicators import indicator_functions
import json
import os
from key_manager import get_key
from cryptography.fernet import Fernet

# Get the encryption key
key = get_key()
cipher_suite = Fernet(key)

def decrypt_data(data):
    return cipher_suite.decrypt(data.encode()).decode()

def load_account_settings():
    account_settings_path = 'account_settings.json'
    
    if not os.path.exists(account_settings_path):
        raise FileNotFoundError(f"{account_settings_path} not found. Please ensure the account settings are saved correctly.")
    
    with open(account_settings_path, 'r') as f:
        account_settings = json.load(f)
    
    account_settings_decrypted = {
        'account': decrypt_data(account_settings['account']),
        'password': decrypt_data(account_settings['password']),
        'server': decrypt_data(account_settings['server']),
        'mt5_path': decrypt_data(account_settings['mt5_path'])
    }
    return account_settings_decrypted

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

def calculate_indicators(data, symbol, timeframe, indicators):
    for indicator in indicators:
        if indicator in indicator_functions:
            try:
                data = indicator_functions[indicator](data, symbol, timeframe)
            except Exception as e:
                print(f"Error calculating {indicator}: {e}")
    return data

def scrape_mt5_data(symbol, timeframe, start_date, end_date, output_file, account, password, server, mt5_path, indicators):
    print(f"Initializing MT5 with path: {mt5_path}")
    if not initialize_mt5(mt5_path):
        return
    
    print(f"Logging in to MT5 account: {account}")
    if not login_mt5(account, password, server):
        return

    print(f"Retrieving historical data for {symbol} from {start_date} to {end_date}...")
    data = get_historical_data(symbol, timeframe, start_date, end_date)
    if data is None:
        mt5.shutdown()
        return
    
    print("Calculating indicators...")
    data = calculate_indicators(data, symbol, timeframe, indicators)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print(f"Saving data to {output_file}...")
    data.to_csv(output_file, index=False)
    
    print("Data scraping completed successfully.")
    
    mt5.shutdown()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 10:
        print("Usage: python MT5_scraper.py <symbol> <timeframe> <start_date> <end_date> <output_file> <account> <password> <server> <mt5_path> <indicators>")
    else:
        symbol = sys.argv[1]
        timeframe = int(sys.argv[2])
        start_date = datetime.strptime(sys.argv[3], '%Y-%m-%d')
        end_date = datetime.strptime(sys.argv[4], '%Y-%m-%d')
        output_file = sys.argv[5]
        account = int(sys.argv[6])
        password = sys.argv[7]
        server = sys.argv[8]
        mt5_path = sys.argv[9]
        indicators = sys.argv[10].split(',')
        scrape_mt5_data(symbol, timeframe, start_date, end_date, output_file, account, password, server, mt5_path, indicators)