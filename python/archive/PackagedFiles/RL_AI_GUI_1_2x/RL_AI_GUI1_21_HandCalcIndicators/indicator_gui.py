import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from indicators.functions import get_available_indicators
from indicators.indicator_library import AppliedPrice, Method  # Import enums

class IndicatorSettingsWindow:
    def __init__(self, parent, indicator_settings):
        self.parent = parent
        self.indicator_settings = indicator_settings if isinstance(indicator_settings, dict) else {}
        self.create_indicator_window()

    def create_indicator_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Indicator Settings")

        # Load available indicators and their parameters
        self.available_indicators, self.indicator_params = get_available_indicators()

        # Debug print to check available indicators
        print(f"Available indicators: {self.available_indicators}")
        print(f"Indicator params: {self.indicator_params}")

        # Create checkboxes and buttons for each indicator
        self.indicator_vars = {}
        for idx, indicator in enumerate(self.available_indicators):
            # Ensure indicator is a string
            if isinstance(indicator, list):
                indicator = indicator[0]
            print(f"Processing indicator: {indicator}")  # Debug print

            # Initialize indicator settings if not already present
            if not isinstance(self.indicator_settings.get(indicator), dict):
                self.indicator_settings[indicator] = {'params': {}, 'is_used': False}

            var = tk.BooleanVar(value=self.indicator_settings[indicator].get('is_used', False))
            self.indicator_vars[indicator] = var
            ttk.Checkbutton(self.window, text=indicator, variable=var).grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Button(self.window, text="Settings", command=lambda ind=indicator: self.open_indicator_settings(ind)).grid(row=idx, column=1, padx=10, pady=5, sticky=tk.W)

        save_button = ttk.Button(self.window, text="Save", command=self.save_indicator_settings)
        save_button.grid(row=len(self.available_indicators), column=0, columnspan=2, pady=10)

    def open_indicator_settings(self, indicator):
        settings_window = tk.Toplevel(self.window)
        settings_window.title(f"{indicator} Settings")

        params = self.indicator_params[indicator.lower()]
        self.param_vars = {}

        for idx, param in enumerate(params):
            ttk.Label(settings_window, text=param).grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
            if param == 'method':
                var = tk.StringVar(value=self.indicator_settings[indicator]['params'].get(param, 'EMA'))
                self.param_vars[param] = var
                combobox = ttk.Combobox(settings_window, textvariable=var, values=[e.name for e in Method])
                combobox.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.EW)
            elif param == 'applied_price':
                var = tk.StringVar(value=self.indicator_settings[indicator]['params'].get(param, 'CLOSE'))
                self.param_vars[param] = var
                combobox = ttk.Combobox(settings_window, textvariable=var, values=[e.name for e in AppliedPrice])
                combobox.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.EW)
            else:
                var = tk.StringVar(value=self.indicator_settings[indicator]['params'].get(param, ''))
                self.param_vars[param] = var
                ttk.Entry(settings_window, textvariable=var).grid(row=idx, column=1, padx=10, pady=5, sticky=tk.EW)

        save_button = ttk.Button(settings_window, text="Save", command=lambda: self.save_params(indicator, settings_window))
        save_button.grid(row=len(params), column=0, columnspan=2, pady=10)

    def save_params(self, indicator, settings_window):
        params = self.indicator_params[indicator.lower()]
        for param in params:
            if not self.param_vars[param].get():
                messagebox.showerror("Error", f"Please fill in all parameters for {indicator}.")
                return

        for param in params:
            self.indicator_settings[indicator]['params'][param] = self.param_vars[param].get()

        settings_window.destroy()

    def save_indicator_settings(self):
        for indicator, var in self.indicator_vars.items():
            self.indicator_settings[indicator]['is_used'] = var.get()

        settings_dir = os.path.join(os.path.dirname(__file__), 'settings')
        indicator_file = os.path.join(settings_dir, 'indicator_settings.json')

        with open(indicator_file, 'w') as f:
            json.dump(self.indicator_settings, f, indent=4)
        messagebox.showinfo("Success", "Settings saved successfully.")