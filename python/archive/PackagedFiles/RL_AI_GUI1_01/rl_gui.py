import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
from datetime import datetime
from start_ai_train import main as start_ai_train_main
import MetaTrader5 as mt5
import threading

def run_script():
    symbol = symbol_entry.get()
    timeframe = timeframe_dict[timeframe_combobox.get()]
    start_date = datetime.strptime(start_date_entry.get(), '%Y-%m-%d')
    end_date = datetime.strptime(end_date_entry.get(), '%Y-%m-%d')
    account = int(account_entry.get())
    password = password_entry.get()
    server = server_entry.get()
    mt5_path = mt5_path_entry.get()
    
    # Start the training in a separate thread to keep the GUI responsive
    threading.Thread(target=start_training, args=(symbol, timeframe, start_date, end_date, account, password, server, mt5_path)).start()

def start_training(symbol, timeframe, start_date, end_date, account, password, server, mt5_path):
    start_ai_train_main(symbol, timeframe, start_date, end_date, account, password, server, mt5_path)

def browse_mt5_path():
    mt5_path = filedialog.askopenfilename(title="Select MetaTrader Terminal", filetypes=[("Executable Files", "*.exe")])
    mt5_path_entry.delete(0, tk.END)
    mt5_path_entry.insert(0, mt5_path)

# Create the main window
root = tk.Tk()
root.title("AI Training Script")

# Create and place the input fields and labels with default values

ttk.Label(root, text="MT5 Account:").grid(column=0, row=0, padx=10, pady=5)
account_entry = ttk.Entry(root)
account_entry.insert(0, '3021640')  # Default value
account_entry.grid(column=1, row=0, padx=10, pady=5)

ttk.Label(root, text="Password:").grid(column=0, row=1, padx=10, pady=5)
password_entry = ttk.Entry(root, show='*')
password_entry.insert(0, 'AItester1!')  # Default value
password_entry.grid(column=1, row=1, padx=10, pady=5)

ttk.Label(root, text="Server:").grid(column=0, row=2, padx=10, pady=5)
server_entry = ttk.Entry(root)
server_entry.insert(0, 'PlexyTrade-Server01')  # Default value
server_entry.grid(column=1, row=2, padx=10, pady=5)

ttk.Label(root, text="MT5 Path:").grid(column=0, row=3, padx=10, pady=5)
mt5_path_entry = ttk.Entry(root)
mt5_path_entry.insert(0, r'C:\Program Files\PlexyTrade MT5 Terminal\terminal64.exe')  # Default value
mt5_path_entry.grid(column=1, row=3, padx=10, pady=5)
browse_button = ttk.Button(root, text="Browse", command=browse_mt5_path)
browse_button.grid(column=2, row=3, padx=10, pady=5)

# Add a separator
ttk.Separator(root, orient='horizontal').grid(column=0, row=4, columnspan=3, sticky='ew', pady=10)

ttk.Label(root, text="Symbol:").grid(column=0, row=5, padx=10, pady=5)
symbol_entry = ttk.Entry(root)
symbol_entry.insert(0, 'XAUUSD')  # Default value
symbol_entry.grid(column=1, row=5, padx=10, pady=5)

ttk.Label(root, text="Timeframe:").grid(column=0, row=6, padx=10, pady=5)
timeframe_combobox = ttk.Combobox(root, values=[
    '1 Minute', '5 Minutes', '15 Minutes', '30 Minutes', '1 Hour', '4 Hours', '1 Day', '1 Week', '1 Month'
])
timeframe_combobox.set('1 Hour')  # Default value
timeframe_combobox.grid(column=1, row=6, padx=10, pady=5)

ttk.Label(root, text="Start Date:").grid(column=0, row=7, padx=10, pady=5)
start_date_entry = DateEntry(root, date_pattern='yyyy-MM-dd')
start_date_entry.set_date('2022-01-01')  # Default value
start_date_entry.grid(column=1, row=7, padx=10, pady=5)

ttk.Label(root, text="End Date:").grid(column=0, row=8, padx=10, pady=5)
end_date_entry = DateEntry(root, date_pattern='yyyy-MM-dd')
end_date_entry.set_date('2022-12-31')  # Default value
end_date_entry.grid(column=1, row=8, padx=10, pady=5)

# Create and place the run button
run_button = ttk.Button(root, text="Run Script", command=run_script)
run_button.grid(column=0, row=9, columnspan=3, padx=10, pady=10)

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

# Add copyright and version number
ttk.Label(root, text="© UpAllNightSpyke").grid(column=0, row=10, columnspan=2, padx=10, pady=5, sticky='w')
ttk.Label(root, text="Version 1.00a").grid(column=2, row=10, padx=10, pady=5, sticky='e')

# Start the GUI event loop
root.mainloop()