import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from indicators.functions import get_available_indicators
from indicators.indicator_library import AppliedPrice, Method  # Import enums
from appdirs import user_data_dir  # Import for user data directory
from indicator_settings_gui import IndicatorSpecificSettingsWindow


class IndicatorSettingsWindow:
    def __init__(self, parent, indicator_settings, user_data_dir):  # Add user_data_dir
        self.parent = parent
        self.indicator_settings = indicator_settings if isinstance(indicator_settings, dict) else {}
        self.user_data_dir = user_data_dir  # Store user_data_dir
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
        params = self.indicator_params[indicator.lower()]
        self.param_vars = {}

        # Create the IndicatorSpecificSettingsWindow instance FIRST
        settings_window = IndicatorSpecificSettingsWindow(
            self.window, self, indicator, self.indicator_settings, params, self.user_data_dir
        )

    def save_params(self, indicator, settings_window):
        params = self.indicator_params[indicator.lower()]
        for param in params:
            if not self.param_vars[param].get():
                messagebox.showerror("Error", f"Please fill in all parameters for {indicator}.")
                return

        for param in params:
            self.indicator_settings[indicator]['params'][param] = self.param_vars[param].get()

        # Save RSI overbought and oversold levels
        if indicator.lower() == 'rsi':
            self.indicator_settings[indicator]['params']['overbought'] = self.param_vars['overbought'].get()
            self.indicator_settings[indicator]['params']['oversold'] = self.param_vars['oversold'].get()

        settings_window.destroy()

    def save_indicator_settings(self):
        for indicator, var in self.indicator_vars.items():
            self.indicator_settings[indicator]['is_used'] = var.get()

        # Construct the correct path to the settings file
        settings_dir = os.path.join(self.user_data_dir, 'settings')  # Use user_data_dir
        os.makedirs(settings_dir, exist_ok=True)
        indicator_file = os.path.join(settings_dir, 'indicator_settings.json')

        with open(indicator_file, 'w') as f:
            json.dump(self.indicator_settings, f, indent=4)
        messagebox.showinfo("Success", "Settings saved successfully.")