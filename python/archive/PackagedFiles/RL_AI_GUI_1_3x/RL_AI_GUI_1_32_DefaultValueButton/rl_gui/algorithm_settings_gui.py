import tkinter as tk
from tkinter import ttk

class AlgorithmSpecificSettingsWindow:
    def __init__(self, parent, main_window, algorithm, algorithm_settings, params):
        self.parent = parent
        self.main_window = main_window
        self.algorithm = algorithm
        self.algorithm_settings = algorithm_settings
        self.params = params
        self.create_algorithm_specific_window()

    def create_algorithm_specific_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"{self.algorithm} Settings")

        # Ensure self.algorithm_settings[self.algorithm] is a dictionary
        if not isinstance(self.algorithm_settings.get(self.algorithm), dict):
            self.algorithm_settings[self.algorithm] = {'params': {}}

        # Create input fields for each parameter
        self.param_vars = {}
        for idx, (param, default_value) in enumerate(self.params.items()):
            var = tk.StringVar(value=self.algorithm_settings[self.algorithm]['params'].get(param, default_value))
            self.param_vars[param] = var
            ttk.Label(self.window, text=param).grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Entry(self.window, textvariable=var).grid(row=idx, column=1, padx=10, pady=5, sticky=tk.EW)

        save_button = ttk.Button(self.window, text="Save", command=self.save_algorithm_specific_settings)
        save_button.grid(row=len(self.params), column=0, columnspan=2, pady=10)

    def save_algorithm_specific_settings(self):
        # Save the parameter values
        if not isinstance(self.algorithm_settings.get(self.algorithm), dict):
            self.algorithm_settings[self.algorithm] = {'params': {}}
        for param, var in self.param_vars.items():
            self.algorithm_settings[self.algorithm]['params'][param] = var.get()
        
        print(f"Settings for {self.algorithm} saved.")
        self.window.destroy()

        # Call the save_to_file method from the main window
        self.main_window.save_to_file()