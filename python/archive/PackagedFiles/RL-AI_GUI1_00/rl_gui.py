import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from start_ai_train import main as start_ai_train_main
import MetaTrader5 as mt5

def run_script():
    symbol = symbol_entry.get()
    timeframe = timeframe_dict[timeframe_combobox.get()]
    start_date = datetime.strptime(start_date_entry.get(), '%Y-%m-%d')
    end_date = datetime.strptime(end_date_entry.get(), '%Y-%m-%d')
    
    start_ai_train_main(symbol, timeframe, start_date, end_date)

# Create the main window
root = tk.Tk()
root.title("AI Training Script")

# Create and place the input fields and labels with default values
ttk.Label(root, text="Symbol:").grid(column=0, row=0, padx=10, pady=5)
symbol_entry = ttk.Entry(root)
symbol_entry.insert(0, 'XAUUSD')  # Default value
symbol_entry.grid(column=1, row=0, padx=10, pady=5)

ttk.Label(root, text="Timeframe:").grid(column=0, row=1, padx=10, pady=5)
timeframe_combobox = ttk.Combobox(root, values=[
    '1 Minute', '5 Minutes', '15 Minutes', '30 Minutes', '1 Hour', '4 Hours', '1 Day', '1 Week', '1 Month'
])
timeframe_combobox.set('1 Hour')  # Default value
timeframe_combobox.grid(column=1, row=1, padx=10, pady=5)

ttk.Label(root, text="Start Date:").grid(column=0, row=2, padx=10, pady=5)
start_date_entry = DateEntry(root, date_pattern='yyyy-MM-dd')
start_date_entry.set_date('2022-01-01')  # Default value
start_date_entry.grid(column=1, row=2, padx=10, pady=5)

ttk.Label(root, text="End Date:").grid(column=0, row=3, padx=10, pady=5)
end_date_entry = DateEntry(root, date_pattern='yyyy-MM-dd')
end_date_entry.set_date('2022-12-31')  # Default value
end_date_entry.grid(column=1, row=3, padx=10, pady=5)

# Create and place the run button
run_button = ttk.Button(root, text="Run Script", command=run_script)
run_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

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

# Start the GUI event loop
root.mainloop()