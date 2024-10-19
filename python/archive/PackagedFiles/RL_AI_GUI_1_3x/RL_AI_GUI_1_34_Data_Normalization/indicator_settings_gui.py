import tkinter as tk
from tkinter import ttk
from indicators.indicator_library import AppliedPrice, Method
import os
from appdirs import user_data_dir  # Import for user data directory

class IndicatorSpecificSettingsWindow:
    def __init__(self, parent, main_window, indicator, indicator_settings, params, user_data_dir):  # Add user_data_dir
        self.parent = parent
        self.main_window = main_window
        self.indicator = indicator
        self.indicator_settings = indicator_settings
        self.params = params
        self.user_data_dir = user_data_dir  # Store user_data_dir
        self.create_indicator_specific_window()

    def create_indicator_specific_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"{self.indicator} Settings")

        # Ensure self.indicator_settings[self.indicator] is a dictionary
        if not isinstance(self.indicator_settings.get(self.indicator), dict):
            self.indicator_settings[self.indicator] = {'params': {}, 'is_used': False}

        # Create input fields for each parameter
        self.param_vars = {}
        for idx, param in enumerate(self.params):
            if param in ['method', 'applied_price']:
                var = tk.StringVar(value=self.indicator_settings[self.indicator]['params'].get(param, ''))
                self.param_vars[param] = var
                ttk.Label(self.window, text=param).grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
                ttk.Combobox(self.window, textvariable=var, values=[e.name for e in (Method if param == 'method' else AppliedPrice)]).grid(row=idx, column=1, padx=10, pady=5, sticky=tk.EW)
            else:
                var = tk.StringVar(value=self.indicator_settings[self.indicator]['params'].get(param, ''))
                self.param_vars[param] = var
                ttk.Label(self.window, text=param).grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
                ttk.Entry(self.window, textvariable=var).grid(row=idx, column=1, padx=10, pady=5, sticky=tk.EW)

        save_button = ttk.Button(self.window, text="Save", command=self.save_indicator_specific_settings)
        save_button.grid(row=len(self.params), column=0, columnspan=2, pady=10)

    def save_indicator_specific_settings(self):
        # Save the parameter values
        if not isinstance(self.indicator_settings.get(self.indicator), dict):
            self.indicator_settings[self.indicator] = {'params': {}, 'is_used': False}
        for param, var in self.param_vars.items():
            self.indicator_settings[self.indicator]['params'][param] = var.get()
        
        print(f"Settings for {self.indicator} saved.")
        self.window.destroy()