from fetch_data import fetch_data, initialize_mt5, login_mt5, get_historical_data, calculate_indicators, save_data_to_csv
from account_gui import AccountWindow
from indicator_gui import IndicatorSettingsWindow
from cryptography.fernet import Fernet
import json
import os
import re
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from indicators.indicator_library import Timeframe
from indicators.functions import indicator_functions, initialize_indicators, get_available_indicators
import MetaTrader5 as mt5
from datetime import datetime
import subprocess

# Initialize indicators
initialize_indicators()

class ForexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Forex Data Fetcher")

        # Initialize account details
        self.account_details = self.load_account_details()

        # Initialize indicator settings
        self.indicator_settings = self.load_indicator_settings()

        # Create input fields for data fetching parameters
        self.create_data_fields()

        # Create buttons
        self.create_buttons()

        # Add footer
        self.add_footer()

        # Populate input fields with settings
        self.populate_input_fields()

    def load_account_details(self):
        settings_dir = os.path.join(os.path.dirname(__file__), 'settings')
        account_file = os.path.join(settings_dir, 'account_settings.json')
        key_file = os.path.join(settings_dir, 'account_key.key')

        if os.path.exists(account_file) and os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
            cipher_suite = Fernet(key)

            with open(account_file, 'rb') as f:
                encrypted_data = f.read()

            decrypted_data = cipher_suite.decrypt(encrypted_data)
            account_details = json.loads(decrypted_data.decode('utf-8'))
            return account_details
        else:
            return {
                'MT5 Path': '',
                'Account': '',
                'Password': '',
                'Server': ''
            }

    def load_indicator_settings(self):
        settings_dir = os.path.join(os.path.dirname(__file__), 'settings')
        indicator_file = os.path.join(settings_dir, 'indicator_settings.json')

        if os.path.exists(indicator_file):
            with open(indicator_file, 'r') as f:
                indicator_settings = json.load(f)
            return indicator_settings if isinstance(indicator_settings, dict) else {}
        else:
            return {}

    def get_all_symbols(self):
        mt5_path = self.account_details.get('MT5 Path', '')
        if not mt5.initialize(mt5_path):
            messagebox.showerror("Error", f"Failed to initialize MT5 with path: {mt5_path}")
            return []
        symbols = mt5.symbols_get()
        mt5.shutdown()
        return [symbol.name for symbol in symbols]

    def create_data_fields(self):
        data_frame = ttk.LabelFrame(self.root, text="Data Fetching Parameters")
        data_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.EW)

        self.data_fields = {
            'Symbol': tk.StringVar(),
            'Timeframe': tk.StringVar(value='H1'),
            'Start Date': tk.StringVar(),
            'End Date': tk.StringVar()
        }

        ttk.Label(data_frame, text="Symbol").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        symbol_combobox = ttk.Combobox(data_frame, textvariable=self.data_fields['Symbol'])
        symbol_combobox.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)
        symbol_combobox['values'] = self.get_all_symbols()
        symbol_combobox.bind('<KeyRelease>', self.update_combobox_values)

        ttk.Label(data_frame, text="Timeframe").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Combobox(data_frame, textvariable=self.data_fields['Timeframe'], values=[e.name for e in Timeframe]).grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

        ttk.Label(data_frame, text="Start Date").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        DateEntry(data_frame, textvariable=self.data_fields['Start Date'], date_pattern='yyyy-mm-dd').grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)

        ttk.Label(data_frame, text="End Date").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        DateEntry(data_frame, textvariable=self.data_fields['End Date'], date_pattern='yyyy-mm-dd').grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)

        save_button = ttk.Button(data_frame, text="Save Settings", command=self.save_settings)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=10)

        account_button = ttk.Button(button_frame, text="Set Account Details", command=self.open_account_window)
        account_button.grid(row=0, column=0, padx=5)

        indicator_button = ttk.Button(button_frame, text="Set Indicator Settings", command=self.open_indicator_window)
        indicator_button.grid(row=0, column=1, padx=5)

        fetch_button = ttk.Button(button_frame, text="Fetch Data", command=self.fetch_data)
        fetch_button.grid(row=0, column=2, padx=5)

        process_button = ttk.Button(button_frame, text="Process Data", command=self.process_data)
        process_button.grid(row=0, column=3, padx=5)

    def open_account_window(self):
        AccountWindow(self.root, self.account_details)

    def open_indicator_window(self):
        IndicatorSettingsWindow(self.root, self.indicator_settings)

    def fetch_data(self):
        fetch_data(self.account_details, self.data_fields)

    def process_data(self):
        try:
            symbol = self.data_fields['Symbol'].get()
            timeframe = Timeframe[self.data_fields['Timeframe'].get()].value

            python_executable = sys.executable
            subprocess.run([python_executable, os.path.join('python', 'preprocess_data.py'), symbol, str(timeframe)])
            
            messagebox.showinfo("Success", "Data processed and saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_settings(self):
        settings_dir = os.path.join(os.path.dirname(__file__), 'settings')
        indicator_file = os.path.join(settings_dir, 'indicator_settings.json')

        if os.path.exists(indicator_file):
            with open(indicator_file, 'r') as f:
                existing_settings = json.load(f)
        else:
            existing_settings = {}

        new_settings = {
            'Symbol': self.data_fields['Symbol'].get(),
            'Timeframe': self.data_fields['Timeframe'].get(),
            'Start Date': self.data_fields['Start Date'].get(),
            'End Date': self.data_fields['End Date'].get()
        }

        existing_settings.update(new_settings)

        with open(indicator_file, 'w') as f:
            json.dump(existing_settings, f, indent=4)
        messagebox.showinfo("Success", "Settings saved successfully.")

    def update_combobox_values(self, event):
        widget = event.widget
        value = widget.get()
        if value == '':
            widget['values'] = self.get_all_symbols()
        else:
            widget['values'] = [symbol for symbol in self.get_all_symbols() if value.lower() in symbol.lower()]

    def populate_input_fields(self):
        if 'Symbol' in self.indicator_settings:
            self.data_fields['Symbol'].set(self.indicator_settings['Symbol'])
        if 'Timeframe' in self.indicator_settings:
            self.data_fields['Timeframe'].set(self.indicator_settings['Timeframe'])
        if 'Start Date' in self.indicator_settings:
            self.data_fields['Start Date'].set(self.indicator_settings['Start Date'])
        if 'End Date' in self.indicator_settings:
            self.data_fields['End Date'].set(self.indicator_settings['End Date'])

    def add_footer(self):
        ttk.Label(self.root, text="© UpAllNightSpyke, 2024").grid(column=0, row=2, columnspan=2, padx=10, pady=5, sticky='w')
        ttk.Label(self.root, text="Version 1.24a").grid(column=2, row=2, padx=10, pady=5, sticky='e')

if __name__ == "__main__":
    root = tk.Tk()
    app = ForexApp(root)
    root.mainloop()