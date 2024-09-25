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
from indicator_window import open_indicator_window
from account_window import open_account_window

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

# Function to run the start_ai_train script
def run_script():
    symbol = symbol_entry.get()
    timeframe = timeframe_dict[timeframe_combobox.get()]
    start_date = datetime.strptime(start_date_entry.get(), '%Y-%m-%d')
    end_date = datetime.strptime(end_date_entry.get(), '%Y-%m-%d')
    selected_indicators = [indicator for indicator, var in indicator_vars.items() if var.get()]
    # Add threading to run the script without freezing the GUI
    threading.Thread(target=start_ai_train_main, args=(symbol, timeframe, start_date, end_date, selected_indicators)).start()

# Main GUI setup
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
indicator_button = tk.Button(root, text="Set Indicator Periods", command=lambda: open_indicator_window(symbol_entry, timeframe_combobox, timeframe_dict, start_date_entry, end_date_entry))
indicator_button.grid(row=5+len(indicators), column=0, columnspan=2, padx=10, pady=5)

# Button to run the script
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=6+len(indicators), column=0, columnspan=2, padx=10, pady=5)

# Add copyright and version number
ttk.Label(root, text="© UpAllNightSpyke").grid(column=0, row=7+len(indicators), columnspan=2, padx=10, pady=5, sticky='w')
ttk.Label(root, text="Version 1.07a").grid(column=2, row=7+len(indicators), padx=10, pady=5, sticky='e')

root.mainloop()