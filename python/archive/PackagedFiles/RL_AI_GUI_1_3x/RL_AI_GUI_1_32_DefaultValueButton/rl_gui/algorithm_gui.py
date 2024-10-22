import sys
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the settings file path relative to the script's location
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'settings', 'algorithm_settings.json')

DEFAULT_SETTINGS = {
    "A2C": {
        "params": {
            "learning_rate": "0.0007",
            "n_steps": "5",
            "gamma": "0.99",
            "gae_lambda": "1.0",
            "ent_coef": "0.01",
            "vf_coef": "0.5",
            "max_grad_norm": "0.5",
            "total_timesteps": "10000"
        }
    },
    "DQN": {
        "params": {
            "learning_rate": "0.001",
            "buffer_size": "100000",
            "learning_starts": "1000",
            "batch_size": "32",
            "tau": "0.005",
            "gamma": "0.99",
            "train_freq": "4",
            "gradient_steps": "1",
            "total_timesteps": "10000"
        }
    },
    "PPO": {
        "params": {
            "learning_rate": "0.0003",
            "n_steps": "2048",
            "batch_size": "64",
            "n_epochs": "10",
            "gamma": "0.99",
            "gae_lambda": "0.95",
            "clip_range": "0.2",
            "total_timesteps": "10000"
        }
    },
    "selected_algorithm": "PPO"
}

class RLModelSelectionWindow:
    def __init__(self, parent, algorithm_settings):
        self.parent = parent
        self.algorithm_settings = self.load_settings()
        self.window = None
        self.algorithm_var = None
        self.algorithms = None
        self.algorithm_params = None
        self.create_model_selection_window()

    def create_model_selection_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("RL Model Selection")

        from rl_algorithms.functions import get_available_algorithms  # Lazy load
        self.algorithms, self.algorithm_params = get_available_algorithms()

        ttk.Label(self.window, text="Select Algorithm:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.algorithm_var = tk.StringVar(value=self.algorithms[0])
        ttk.Combobox(self.window, textvariable=self.algorithm_var, values=self.algorithms).grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        settings_button = ttk.Button(self.window, text="Settings", command=self.open_algorithm_settings)
        settings_button.grid(row=1, column=0, columnspan=2, pady=10)

        save_button = ttk.Button(self.window, text="Save", command=self.save_model_selection)
        save_button.grid(row=2, column=0, pady=10, sticky=tk.W)

        default_button = ttk.Button(self.window, text="Default Settings", command=self.reset_to_default)
        default_button.grid(row=2, column=1, pady=10, sticky=tk.E)

    def open_algorithm_settings(self):
        from rl_gui.algorithm_settings_gui import AlgorithmSpecificSettingsWindow  # Lazy load
        algorithm = self.algorithm_var.get()
        params = self.algorithm_params[algorithm.lower()]
        AlgorithmSpecificSettingsWindow(self.window, self, algorithm, self.algorithm_settings, params)

    def save_model_selection(self):
        algorithm = self.algorithm_var.get()
        self.algorithm_settings['selected_algorithm'] = algorithm
        self.save_to_file()
        messagebox.showinfo("Success", "Algorithm selection saved.")
        self.window.destroy()  # Only destroy the RLModelSelectionWindow

    def reset_to_default(self):
        self.algorithm_settings = DEFAULT_SETTINGS.copy()
        self.save_to_file()
        messagebox.showinfo("Success", "Settings have been reset to default.")
        self.window.destroy()  # Only destroy the RLModelSelectionWindow

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as file:
                return json.load(file)
        return DEFAULT_SETTINGS

    def save_to_file(self):
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(self.algorithm_settings, file, indent=4)

# Example usage
def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    algorithm_settings = {}
    app = RLModelSelectionWindow(root, algorithm_settings)
    root.mainloop()

if __name__ == "__main__":
    main()