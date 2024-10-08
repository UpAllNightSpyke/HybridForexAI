import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet
import json
import os
import importlib.util
from indicators import get_available_indicators

# Define the key file path
key_file_path = 'encryption_key.key'

# Check if the key file exists
if not os.path.exists(key_file_path):
    # Generate a new key and save it to the file
    key = Fernet.generate_key()
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)
else:
    # Load the key from the file
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()

cipher_suite = Fernet(key)

def decrypt_data(data):
    return cipher_suite.decrypt(data.encode()).decode()

def load_account_settings():
    with open('account_settings.json', 'r') as f:
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
    # Expecting start_date and end_date to be datetime objects
    rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
    if rates is None:
        print(f"Failed to get historical data for {symbol}")
        return None
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.rename(columns={'volume': 'real_volume'}, inplace=True)  # Ensure volume column is correctly named
    print(f"Retrieved data columns: {data.columns}")  # Debug line
    return data

def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_available_indicators(indicators_path):
    indicators = {}
    for file_name in os.listdir(indicators_path):
        if file_name.endswith('.py') and file_name != '__init__.py':
            module_name = file_name[:-3]  # Remove thepy extension
            module = import_module_from_file(module_name, os.path.join(indicators_path, file_name))
            indicators[module_name] = module
    print(f"Available indicators: {list(indicators.keys())}")  # Debug line
    return indicators

def calculate_indicators(data, symbol, timeframe, indicators, indicator_settings):
    print(f"Indicators to calculate: {indicators}")  # Debug line
    for indicator in indicators:
        if indicator in indicator_functions:
            try:
                settings = indicator_settings.get(indicator, {})
                print(f"Calculating {indicator} with settings: {settings}")  # Debug line
                print(f"Data columns before calculating {indicator}: {data.columns}")  # Debug line
                data = indicator_functions[indicator].calculate(data, symbol, timeframe, **settings)
                print(f"Calculated {indicator} successfully.")  # Debug line
                print(f"Data columns after calculating {indicator}: {data.columns}")  # Debug line
            except Exception as e:
                print(f"Error calculating {indicator}: {e}")
        else:
            print(f"Indicator function for {indicator} not found.")  # Debug line
    return data

def scrape_mt5_data(symbol, timeframe, start_date, end_date, output_file, account, password, server, mt5_path, indicators, indicator_settings):
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
    data = calculate_indicators(data, symbol, timeframe, indicators, indicator_settings)
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print(f"Saving data to {output_file}...")
    print(f"Data columns before saving: {data.columns}")  # Debug line
    data.to_csv(output_file, sep='\t', index=False)  # Save as TSV
    
    print("Data scraping completed successfully.")
    
    mt5.shutdown()

# Ensure the indicator functions are dynamically loaded
indicators_path = 'D:\\ForexFiles\\ForexGitFolders\\NeuralNetworkEA\\HybridForexAI\\python\\indicators'
indicator_functions = get_available_indicators(indicators_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 11:  # Updated to 11 to include the script name
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
        indicators_path = 'D:\\ForexFiles\\ForexGitFolders\\NeuralNetworkEA\\HybridForexAI\\python\\indicators'
        indicator_functions = get_available_indicators(indicators_path)
        # Filter indicators to ensure only selected ones are passed
        filtered_indicators = [indicator for indicator in indicators if indicator in indicator_functions]
        print(f"Filtered indicators: {filtered_indicators}")  # Debug line
        scrape_mt5_data(symbol, timeframe, start_date, end_date, output_file, account, password, server, mt5_path, filtered_indicators, indicator_functions)