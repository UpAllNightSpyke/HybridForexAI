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

def calculate_indicators(data, indicators, indicator_settings):
    indicator_data = data.copy()
    for indicator_name, settings in indicator_settings.items():
        if indicator_name in ["Symbol", "Timeframe", "Start Date", "End Date"]:
            continue  # Skip non-indicator settings
        print(f"Processing indicator: {indicator_name} with settings: {settings}")
        if isinstance(settings, dict) and settings.get('is_used'):
            indicator_func = indicators.get(indicator_name)
            if indicator_func:
                try:
                    # Call the indicator function with the appropriate parameters
                    print(f"Calculating {indicator_name} using custom function...")
                    indicator_values = indicator_func(data, settings['symbol'], settings['timeframe'], settings['params'])
                    indicator_data = pd.concat([indicator_data, indicator_values], axis=1)
                    print(f"Calculated {indicator_name}: {indicator_values.head()}")
                except Exception as e:
                    print(f"Error calculating {indicator_name}: {e}")
            else:
                print(f"Indicator function for {indicator_name} not found.")
        else:
            print(f"Indicator {indicator_name} is not used or settings are invalid.")
    
    # Remove rows with NaN values in any of the indicator columns
    indicator_data.dropna(inplace=True)
    
    return indicator_data

def save_data_to_csv(symbol, timeframe, start_date, end_date, data, indicator_data, output_dir=None): 
    """Saves data to a CSV file.

    Args:
        symbol (str): The trading symbol.
        timeframe (str): The timeframe of the data.
        start_date (datetime): The start date of the data.
        end_date (datetime): The end date of the data.
        data (pd.DataFrame): The raw price data.
        indicator_data (pd.DataFrame): The calculated indicator data.
        output_dir (str, optional): The directory to save the CSV file. 
                                      Defaults to 'data/raw' relative to the script's location.
    """
    # Get the user data directory
    user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")  # Adjust app_name and author if needed

    # Define the output directory within the user data directory
    output_dir = os.path.join(user_data_path, 'forex_data', 'raw') 

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    combined_data = data.copy()
    for col in indicator_data.columns:
        combined_data[col] = indicator_data[col]
    
    print(f"Combined DataFrame before saving:\n{combined_data.head()}")

    output_file = os.path.join(output_dir, f"{symbol}_{timeframe}.csv")
    combined_data.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
    
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
        timeframe = Timeframe[data_fields['Timeframe'].get()].value
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
                indicator_data = calculate_indicators(data, indicator_functions, indicator_settings) # Calculate first

                save_data_to_csv(symbol, timeframe, start_date, end_date, data, indicator_data)  # Then save

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