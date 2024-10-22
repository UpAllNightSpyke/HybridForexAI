import tkinter as tk
from tkinter import messagebox
import json

def open_indicator_window(symbol_entry, timeframe_combobox, timeframe_dict, start_date_entry, end_date_entry):
    indicator_window = tk.Toplevel()
    indicator_window.title("Indicator Input GUI")

    # Create input fields for each indicator's period
    tk.Label(indicator_window, text="RSI Period:").grid(row=0, column=0, padx=5, pady=5)
    rsi_period_entry = tk.Entry(indicator_window)
    rsi_period_entry.grid(row=0, column=1, padx=5, pady=5)
    rsi_period_entry.insert(0, "14")  # Default value

    tk.Label(indicator_window, text="SMA Period:").grid(row=1, column=0, padx=5, pady=5)
    sma_period_entry = tk.Entry(indicator_window)
    sma_period_entry.grid(row=1, column=1, padx=5, pady=5)
    sma_period_entry.insert(0, "200")  # Default value

    tk.Label(indicator_window, text="EMA Period:").grid(row=2, column=0, padx=5, pady=5)
    ema_period_entry = tk.Entry(indicator_window)
    ema_period_entry.grid(row=2, column=1, padx=5, pady=5)
    ema_period_entry.insert(0, "5")

    def on_submit():
        try:
            indicator_periods = {
                'RSI': int(rsi_period_entry.get()),
                'SMA': int(sma_period_entry.get()),
                'EMA': int(ema_period_entry.get())
            }
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values for all indicator periods.")
            return
        
        settings = {
            'symbol': symbol_entry.get(),
            'timeframe': timeframe_dict[timeframe_combobox.get()],
            'start_date': start_date_entry.get(),
            'end_date': end_date_entry.get(),
            'indicator_periods': indicator_periods
        }
        
        with open('indicator_settings.json', 'w') as f:
            json.dump(settings, f)
        
        messagebox.showinfo("Success", "Indicator settings saved successfully!")
        indicator_window.destroy()

    tk.Button(indicator_window, text="Submit", command=on_submit).grid(row=3, column=0, columnspan=2, pady=10)