import tkinter as tk
from tkinter import ttk
import json
import os
from indicators.functions import get_available_indicators
from indicator_settings_gui import IndicatorSpecificSettingsWindow

class IndicatorSettingsWindow:
    def __init__(self, parent, indicator_settings):
        self.parent = parent
        self.indicator_settings = indicator_settings
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
        params = self.indicator_params.get(indicator.lower(), [])
        IndicatorSpecificSettingsWindow(self.window, self, indicator, self.indicator_settings, params)

    def save_indicator_settings(self):
        for indicator, var in self.indicator_vars.items():
            if indicator not in self.indicator_settings:
                self.indicator_settings[indicator] = {'params': {}, 'is_used': var.get()}
            else:
                self.indicator_settings[indicator]['is_used'] = var.get()
        
        # Save indicator settings to a file
        self.save_to_file()
        self.window.destroy()

    def save_to_file(self):
        settings_dir = os.path.join(os.path.dirname(__file__), 'settings')
        os.makedirs(settings_dir, exist_ok=True)
        with open(os.path.join(settings_dir, 'indicator_settings.json'), 'w') as f:
            json.dump(self.indicator_settings, f, indent=4)

        print("Indicator settings saved successfully.")