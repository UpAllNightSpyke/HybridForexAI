import MetaTrader5 as mt5
import pandas as pd
import json
import os
from datetime import datetime
from indicators.functions import initialize_indicators, get_available_indicators
from indicators import indicator_functions
from indicators.indicator_library import Timeframe, TIMEFRAME_MAP
from tkinter import messagebox
import subprocess
from appdirs import user_data_dir  # Import for user data directory


# Initialize indicators
initialize_indicators()

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
    print(f"Fetching historical data for {symbol} from {start_date} to {end_date} with timeframe {timeframe}")
    
    if not mt5.symbol_select(symbol, True):
        print(f"Symbol {symbol} is not available.")
        return None
    
    try:
        timeframe_enum = Timeframe(int(timeframe))
    except ValueError:
        print(f"Timeframe {timeframe} is not valid.")
        return None
    
    if start_date >= end_date:
        print("Start date must be earlier than end date.")
        return None
    
    rates = mt5.copy_rates_range(symbol, TIMEFRAME_MAP[timeframe_enum], start_date, end_date)
    if rates is None or len(rates) == 0:
        print(f"Failed to get historical data for {symbol}")
        print(f"Error code: {mt5.last_error()}")
        return None
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    return data

def calculate_indicators(data, indicator_functions, indicator_settings):
    """Calculates the selected technical indicators using the provided data and settings."""
    indicator_data = {}

    for indicator_name in indicator_functions:  # Iterate through available indicators
        settings = indicator_settings.get(indicator_name)  # Get settings for the current indicator
        if settings is None or not settings.get('is_used'):
            print(f"Indicator {indicator_name} is not used or settings are invalid.")
            continue

        try:
            # Call the corresponding function from the indicator_functions dictionary
            indicator_func = indicator_functions[indicator_name]

            # Get the parameters from the settings
            params = settings.get('params', {})

            # Call the indicator function with the parameters
            result = indicator_func(data, indicator_settings['Symbol'], indicator_settings['Timeframe'], params)

            indicator_data[indicator_name] = result
            print(f"Calculated {indicator_name}: ", result)  # Print the calculated indicator data

        except Exception as e:
            print(f"Error processing indicator: {indicator_name} with settings: {settings}")
            print(f"Error details: {e}")

    return indicator_data

def save_data_to_csv(filepath, data, indicator_data):  # Use filepath directly
    """Saves data to a CSV file with the specified filepath."""

    combined_data = data.copy()
    for col in indicator_data.columns:
        combined_data[col] = indicator_data[col]

    print(f"Combined DataFrame before saving:\n{combined_data.head()}")

    combined_data.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")
    
def load_indicator_settings():
    # Get the user data directory
    user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")  # Adjust app_name and author if needed
    settings_dir = os.path.join(user_data_path, 'settings')
    indicator_file = os.path.join(settings_dir, 'indicator_settings.json')

    if os.path.exists(indicator_file):
        with open(indicator_file, 'r') as f:
            indicator_settings = json.load(f)
        return indicator_settings
    else:
        print("Indicator settings file not found.")
        return None

def fetch_data(account_details, data_fields):
    try:
        initialize_indicators()
        indicators, _ = get_available_indicators()
        print(f"Available indicators: {indicators}")

        mt5_path = account_details['MT5 Path']
        account = int(account_details['Account'])
        password = account_details['Password']
        server = account_details['Server']

        symbol = data_fields['Symbol'].get()
        timeframe_str = data_fields['Timeframe'].get()  # Get timeframe as string
        timeframe = Timeframe[timeframe_str].value  # Convert to enum value
        start_date = datetime.strptime(data_fields['Start Date'].get(), '%Y-%m-%d')
        end_date = datetime.strptime(data_fields['End Date'].get(), '%Y-%m-%d')

        if initialize_mt5(mt5_path) and login_mt5(account, password, server):
            data = get_historical_data(symbol, timeframe, start_date, end_date)
            if data is not None:
                indicator_settings = load_indicator_settings()
                if indicator_settings is None:
                    messagebox.showerror("Error", "Failed to load indicator settings.")
                    return

                add_symbol_and_timeframe_to_settings(indicator_settings, symbol, timeframe)
                indicator_data = calculate_indicators(data, indicator_functions, indicator_settings)

                # Construct filename with symbol, timeframe, start date, and end date
                filename = f"{symbol}_{timeframe}_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.csv"
                filepath = os.path.join(user_data_dir, 'forex_data', 'raw', filename)

                save_data_to_csv(filepath, data, indicator_data)  # Use the constructed filepath

                messagebox.showinfo("Success", "Data fetched and saved successfully.")

            else:
                messagebox.showerror("Error", "Failed to fetch historical data.")
            mt5.shutdown()
        else:
            messagebox.showerror("Error", "Failed to initialize or login to MT5.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_symbol_and_timeframe_to_settings(indicator_settings, symbol, timeframe):
    for indicator_name, settings in indicator_settings.items():
        if isinstance(settings, dict):
            settings['symbol'] = symbol
            settings['timeframe'] = timeframe

if __name__ == "__main__":
    indicator_settings = load_indicator_settings()
    if indicator_settings is None:
        exit()

    symbol = indicator_settings['Symbol']
    timeframe = indicator_settings['Timeframe']
    start_date = datetime.strptime(indicator_settings['Start Date'], '%Y-%m-%d')
    end_date = datetime.strptime(indicator_settings['End Date'], '%Y-%m-%d')
    mt5_path = 'path_to_mt5_terminal'
    account = 'your_account_number'
    password = 'your_password'
    server = 'your_server'

    available_symbols = mt5.symbols_get()
    print("Available symbols:", [s.name for s in available_symbols])

    print("Available timeframes:", [attr for attr in dir(mt5) if attr.startswith('TIMEFRAME_')])

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info:
        print(f"Symbol {symbol} info: {symbol_info}")
    else:
        print(f"Symbol {symbol} not found")

    indicator_settings.pop('Symbol')
    indicator_settings.pop('Timeframe')
    indicator_settings.pop('Start Date')
    indicator_settings.pop('End Date')

    if initialize_mt5(mt5_path) and login_mt5(account, password, server):
        data = get_historical_data(symbol, timeframe, start_date, end_date)
        if data is not None:
            indicators = indicator_functions
            indicator_data = calculate_indicators(data, indicators, indicator_settings)
            save_data_to_csv(symbol, timeframe, start_date, end_date, data, indicator_data)
        mt5.shutdown()