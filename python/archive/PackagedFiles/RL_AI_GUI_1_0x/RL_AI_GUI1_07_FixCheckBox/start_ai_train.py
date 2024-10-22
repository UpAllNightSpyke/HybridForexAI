import os
import json
from datetime import datetime
from MT5_scraper import scrape_mt5_data
from format_data import format_data
from train_rl_agent import main as train_rl_agent_main
import MetaTrader5 as mt5
from indicators import get_available_indicators
from cryptography.fernet import Fernet

def decrypt_data(data, cipher_suite):
    return cipher_suite.decrypt(data.encode()).decode()

def load_settings():
    account_settings_path = 'account_settings.json'
    indicator_settings_path = 'indicator_settings.json'
    
    # Print the current working directory for debugging
    print(f"Current working directory: {os.getcwd()}")
    
    if not os.path.exists(account_settings_path):
        raise FileNotFoundError(f"{account_settings_path} not found. Please ensure the account settings are saved correctly.")
    
    if not os.path.exists(indicator_settings_path):
        raise FileNotFoundError(f"{indicator_settings_path} not found. Please ensure the indicator settings are saved correctly.")
    
    with open(account_settings_path, 'r') as f:
        account_settings = json.load(f)
    
    with open(indicator_settings_path, 'r') as f:
        indicator_settings = json.load(f)
    
    # Load the encryption key
    with open('encryption_key.key', 'rb') as key_file:
        key = key_file.read()
    
    cipher_suite = Fernet(key)
    
    account_settings_decrypted = {
        'account': decrypt_data(account_settings['account'], cipher_suite),
        'password': decrypt_data(account_settings['password'], cipher_suite),
        'server': decrypt_data(account_settings['server'], cipher_suite),
        'mt5_path': decrypt_data(account_settings['mt5_path'], cipher_suite)
    }
    
    return account_settings_decrypted, indicator_settings

def main(symbol, timeframe, start_date, end_date, selected_indicators):
    account_settings, indicator_settings = load_settings()
    
    # Use the parameters passed to the function
    indicator_periods = indicator_settings['indicator_periods']
    
    account = int(account_settings['account'])
    password = account_settings['password']
    server = account_settings['server']
    mt5_path = account_settings['mt5_path']
    
    indicators = get_available_indicators()
    
    # Filter indicators based on user selection
    indicators = [indicator for indicator in indicators if indicator in selected_indicators]
    
    # Debug prints
    print(f"Symbol: {symbol}")
    print(f"Timeframe: {timeframe}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Account: {account}")
    print(f"Password: {password}")
    print(f"Server: {server}")
    print(f"MT5 Path: {mt5_path}")
    print(f"Indicators: {indicators}")
    print(f"Selected Indicators: {selected_indicators}")
    
    raw_output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'raw', 'MarketData.csv')
    formatted_output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'processed', 'MarketData_Prepared.tsv')
    
    # Ensure the directories exist
    os.makedirs(os.path.dirname(raw_output_file), exist_ok=True)
    os.makedirs(os.path.dirname(formatted_output_file), exist_ok=True)

    # Step 1: Scrape data from MT5
    scrape_mt5_data(symbol, timeframe, start_date, end_date, raw_output_file, account, password, server, mt5_path, indicators)

    # Step 2: Format the scraped data
    format_data(raw_output_file, formatted_output_file)

    # Step 3: Train the RL agent
    train_rl_agent_main()

if __name__ == "__main__":
    account_settings, indicator_settings = load_settings()
    main(
        indicator_settings['symbol'],
        indicator_settings['timeframe'],
        datetime.strptime(indicator_settings['start_date'], '%Y-%m-%d'),
        datetime.strptime(indicator_settings['end_date'], '%Y-%m-%d'),
        indicator_settings['indicator_periods']
    )