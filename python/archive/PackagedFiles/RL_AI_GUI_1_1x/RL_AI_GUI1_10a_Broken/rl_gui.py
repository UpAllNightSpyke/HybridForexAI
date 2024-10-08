import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from start_ai_train import main as start_ai_train_main
import MetaTrader5 as mt5
import threading
import json
import os
import importlib.util
from indicator_window import open_indicator_window
from account_window import open_account_window
from indicators import get_available_indicators

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

# Path to the indicators folder
indicators_path = 'D:\\ForexFiles\\ForexGitFolders\\NeuralNetworkEA\\HybridForexAI\\python\\indicators'

# Function to dynamically import a module
def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Function to get available indicators by searching the indicators folder
def get_available_indicators():
    indicators = []
    for file_name in os.listdir(indicators_path):
        if file_name.endswith('.py') and file_name != '__init__.py':
            indicators.append(file_name[:-3])  # Remove the .py extension
    return indicators

# Function to open the indicator settings window
def open_indicator_window(indicator_name):
    indicator_window = tk.Toplevel()
    indicator_window.title(f"{indicator_name} Settings")

    # Dynamically import the indicator module to get its parameters
    indicator_module = import_module_from_file(indicator_name, os.path.join(indicators_path, f'{indicator_name}.py'))
    params = getattr(indicator_module, 'indicator_params', [])

    # Create input fields for each parameter
    entries = {}
    for i, param in enumerate(params):
        tk.Label(indicator_window, text=f"{param}:").grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(indicator_window)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entry.insert(0, "0")  # Default value
        entries[param] = entry

    def on_submit():
        try:
            settings = {param: int(entry.get()) for param, entry in entries.items()}
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values for all parameters.")
            return
        
        settings['indicator'] = indicator_name
        
        # Load existing settings if the file exists
        if os.path.exists('indicator_settings.json'):
            with open('indicator_settings.json', 'r') as f:
                all_settings = json.load(f)
        else:
            all_settings = {}

        # Update the settings for the current indicator
        all_settings[indicator_name] = settings

        # Save the updated settings back to the file
        with open('indicator_settings.json', 'w') as f:
            json.dump(all_settings, f, indent=4)
        
        messagebox.showinfo("Success", f"{indicator_name} settings saved successfully!")
        indicator_window.destroy()

    tk.Button(indicator_window, text="Submit", command=on_submit).grid(row=len(params), column=0, columnspan=2, pady=10)

# Function to run the start_ai_train script
def run_script():
    symbol = symbol_entry.get()
    timeframe = timeframe_dict[timeframe_combobox.get()]
    start_date = datetime.strptime(start_date_entry.get(), '%Y-%m-%d')
    end_date = datetime.strptime(end_date_entry.get(), '%Y-%m-%d')
    selected_indicators = [indicator for indicator, var in indicator_vars.items() if var.get()]

    # Load settings for each selected indicator
    if os.path.exists('indicator_settings.json'):
        with open('indicator_settings.json', 'r') as f:
            all_settings = json.load(f)
    else:
        all_settings = {}

    indicator_settings = {indicator: all_settings.get(indicator, {}) for indicator in selected_indicators}

    # Debug prints
    print(f"Selected Indicators: {selected_indicators}")
    print(f"Indicator Settings: {indicator_settings}")

    # Add threading to run the script without freezing the GUI
    threading.Thread(target=start_ai_train_main, args=(symbol, timeframe, start_date, end_date, selected_indicators, indicator_settings)).start()
    
# Initialize the main window
root = tk.Tk()
root.title("AI Training Script")

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

# Indicator toggle boxes and buttons
indicator_vars = {}
indicators = get_available_indicators()
for i, indicator in enumerate(indicators):
    var = tk.BooleanVar(value=True)
    indicator_vars[indicator] = var
    tk.Checkbutton(root, text=indicator, variable=var).grid(row=5+i*2, column=0, columnspan=2, padx=10, pady=5)
    tk.Button(root, text=f"Set {indicator} Variables", command=lambda ind=indicator: open_indicator_window(ind)).grid(row=6+i*2, column=0, columnspan=2, padx=10, pady=5)

# Button to run the script
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=5+len(indicators)*2, column=0, columnspan=2, padx=10, pady=5)

# Add copyright and version number
ttk.Label(root, text="© UpAllNightSpyke").grid(column=0, row=6+len(indicators)*2, columnspan=2, padx=10, pady=5, sticky='w')
ttk.Label(root, text="Version 1.10a").grid(column=2, row=6+len(indicators)*2, padx=10, pady=5, sticky='e')

root.mainloop()