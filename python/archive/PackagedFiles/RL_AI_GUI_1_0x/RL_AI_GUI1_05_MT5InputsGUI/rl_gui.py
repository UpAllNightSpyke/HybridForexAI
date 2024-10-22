import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from start_ai_train import main as start_ai_train_main
import MetaTrader5 as mt5
import threading
from indicators import get_available_indicators
import json
import os

# Dictionary to map combobox selection to MT5 timeframe constants
timeframe_dict = {
    '1 Minute': mt5.TIMEFRAME_M1,
    '5 Minutes': mt5.TIMEFRAME_M5,
    '15 Minutes': mt5.TIMEFRAME_M15,
    '30 Minutes': mt5.TIMEFRAME_M30,
    '1 Hour': mt5.TIMEFRAME_H1,
    '4 Hours': mt5.TIMEFRAME_H4,
    '1 Day': mt5.TIMEFRAME_D1,
    '1 Week': mt5.TIMEFRAME_W1,
    '1 Month': mt5.TIMEFRAME_MN1
}

# Initialize the main window
root = tk.Tk()
root.title("AI Training Script")

# Function to save indicator settings
def save_indicator_settings(settings):
    with open('indicator_settings.json', 'w') as f:
        json.dump(settings, f)
    messagebox.showinfo("Success", "Indicator settings saved successfully!")

# Function to open the secondary window for indicator inputs
def open_indicator_window():
    indicator_window = tk.Toplevel()
    indicator_window.title("Indicator Input GUI")

    # Create input fields for each indicator's period
    tk.Label(indicator_window, text="RSI Period:").grid(row=0, column=0, padx=5, pady=5)
    rsi_period_entry = tk.Entry(indicator_window)
    rsi_period_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(indicator_window, text="SMA Period:").grid(row=1, column=0, padx=5, pady=5)
    sma_period_entry = tk.Entry(indicator_window)
    sma_period_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(indicator_window, text="EMA Period:").grid(row=2, column=0, padx=5, pady=5)
    ema_period_entry = tk.Entry(indicator_window)
    ema_period_entry.grid(row=2, column=1, padx=5, pady=5)

    def on_submit():
        indicator_periods = {
            'RSI': int(rsi_period_entry.get()),
            'SMA': int(sma_period_entry.get()),
            'EMA': int(ema_period_entry.get())
        }
        
        settings = {
            'symbol': symbol_entry.get(),
            'timeframe': timeframe_dict[timeframe_combobox.get()],
            'start_date': start_date_entry.get(),
            'end_date': end_date_entry.get(),
            'indicator_periods': indicator_periods
        }
        save_indicator_settings(settings)
        indicator_window.destroy()

    submit_button = tk.Button(indicator_window, text="Save Settings", command=on_submit)
    submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Function to open the MT5 account settings window
def open_account_window():
    account_window = tk.Toplevel()
    account_window.title("MT5 Account Information")

    # Create input fields for MT5 account information
    tk.Label(account_window, text="Account Number:").grid(row=0, column=0, padx=5, pady=5)
    account_entry = tk.Entry(account_window)
    account_entry.grid(row=0, column=1, padx=5, pady=5)
    account_entry.insert(0, "3021640")  # Default value

    tk.Label(account_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(account_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)
    password_entry.insert(0, "AItester1!")  # Default value

    tk.Label(account_window, text="Server:").grid(row=2, column=0, padx=5, pady=5)
    server_entry = tk.Entry(account_window)
    server_entry.grid(row=2, column=1, padx=5, pady=5)
    server_entry.insert(0, "PlexyTrade-Server01")  # Default value

    tk.Label(account_window, text="MT5 Path:").grid(row=3, column=0, padx=5, pady=5)
    mt5_path_entry = tk.Entry(account_window)
    mt5_path_entry.grid(row=3, column=1, padx=5, pady=5)
    mt5_path_entry.insert(0, "C:\\Program Files\\PlexyTrade MT5 Terminal\\terminal64.exe")  # Default value

    def browse_mt5_path():
        file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if file_path:
            mt5_path_entry.delete(0, tk.END)
            mt5_path_entry.insert(0, file_path)

    browse_button = tk.Button(account_window, text="Browse", command=browse_mt5_path)
    browse_button.grid(row=3, column=2, padx=5, pady=5)

    def on_submit():
        account_settings = {
            'account': int(account_entry.get()),
            'password': password_entry.get(),
            'server': server_entry.get(),
            'mt5_path': mt5_path_entry.get()
        }
        with open('account_settings.json', 'w') as f:
            json.dump(account_settings, f)
        messagebox.showinfo("Success", "Account settings saved successfully!")
        account_window.destroy()

    submit_button = tk.Button(account_window, text="Save Settings", command=on_submit)
    submit_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Function to run the start_ai_train script
def run_script():
    symbol = symbol_entry.get()
    timeframe = timeframe_dict[timeframe_combobox.get()]
    start_date = datetime.strptime(start_date_entry.get(), '%Y-%m-%d')
    end_date = datetime.strptime(end_date_entry.get(), '%Y-%m-%d')
    selected_indicators = {indicator: var.get() for indicator, var in indicator_vars.items() if var.get()}
    # Add threading to run the script without freezing the GUI
    threading.Thread(target=start_ai_train_main, args=(symbol, timeframe, start_date, end_date, selected_indicators)).start()

# Create input fields for common parameters
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Button to open the MT5 account settings window
account_button = tk.Button(root, text="Set Account Settings", command=open_account_window)
account_button.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

tk.Label(root, text="Symbol:").grid(row=1, column=0, padx=10, pady=5)
symbol_entry = tk.Entry(root)
symbol_entry.grid(row=1, column=1, padx=10, pady=5)
symbol_entry.insert(0, "XAUUSD")  # Set default value for Symbol

tk.Label(root, text="Timeframe:").grid(row=2, column=0, padx=10, pady=5)
timeframe_combobox = ttk.Combobox(root, values=list(timeframe_dict.keys()))
timeframe_combobox.grid(row=2, column=1, padx=10, pady=5)
timeframe_combobox.set("1 Hour")  # Set default value for Timeframe

tk.Label(root, text="Start Date:").grid(row=3, column=0, padx=10, pady=5)
start_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
start_date_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="End Date:").grid(row=4, column=0, padx=10, pady=5)
end_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
end_date_entry.grid(row=4, column=1, padx=10, pady=5)

# Indicator toggle boxes
indicator_vars = {}
indicators = get_available_indicators()
for i, indicator in enumerate(indicators):
    var = tk.BooleanVar(value=True)
    indicator_vars[indicator] = var
    tk.Checkbutton(root, text=indicator, variable=var).grid(row=5+i, column=0, columnspan=2, padx=10, pady=5)

# Button to open the secondary window for indicator inputs
indicator_button = tk.Button(root, text="Set Indicator Periods", command=open_indicator_window)
indicator_button.grid(row=5+len(indicators), column=0, columnspan=2, padx=10, pady=5)

# Button to run the script
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=6+len(indicators), column=0, columnspan=2, padx=10, pady=5)

# Add copyright and version number
ttk.Label(root, text="© UpAllNightSpyke").grid(column=0, row=7+len(indicators), columnspan=2, padx=10, pady=5, sticky='w')
ttk.Label(root, text="Version 1.05a").grid(column=2, row=7+len(indicators), padx=10, pady=5, sticky='e')

root.mainloop()