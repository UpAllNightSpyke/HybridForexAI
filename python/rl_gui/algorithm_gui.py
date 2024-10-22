import os
import json
from appdirs import user_data_dir  # Import for user data directory
############################################ UI Imports ############################################
import tkinter as tk
from tkinter import ttk, messagebox, messagebox, filedialog
############################################ RL Imports ############################################
from rl_algorithms.utils import get_available_algorithms  # Import here
from rl_algorithms.functions import initialize_algorithms, rl_algorithms
############################################ HMM Imports ############################################
import pandas as pd
from hmmlearn import hmm
from ai_utils.train_hmm import train_hmm_model

def get_available_algorithms():
    initialize_algorithms()  # Call initialize_algorithms here
    return rl_algorithms

# Get the user data directory
user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")  # Adjust app_name and author if needed
# Define the settings file path within the user data directory
SETTINGS_FILE = os.path.join(user_data_path, 'settings', 'algorithm_settings.json')

DEFAULT_SETTINGS = {
    "A2C": {
        "params": {
            "learning_rate": 0.0007,
            "n_steps": 5,
            "gamma": 0.99,
            "gae_lambda": 1.0,
            "ent_coef": 0.01,
            "vf_coef": 0.5,
            "max_grad_norm": 0.5,
            "total_timesteps": 10000
        }
    },
    "DQN": {
        "params": {
            "learning_rate": 0.001,
            "buffer_size": 100000,
            "learning_starts": 1000,
            "batch_size": 32,
            "tau": 0.005,
            "gamma": 0.99,
            "train_freq": 4,
            "gradient_steps": 1,
            "total_timesteps": 10000
        }
    },
    "PPO": {
        "params": {
            "learning_rate": 0.0003,
            "n_steps": 2048,
            "batch_size": 64,
            "n_epochs": 10,
            "gamma": 0.99,
            "gae_lambda": 0.95,
            "clip_range": 0.2,
            "total_timesteps": 10000
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
        
        self.load_hmm_label = None

        # Load the last loaded HMM model filename from settings
        if 'loaded_hmm_model' in self.algorithm_settings:
            loaded_model_filename = self.algorithm_settings['loaded_hmm_model']

            # Create the label here, before configuring its text
            self.load_hmm_label = ttk.Label(self.window, text="")
            self.load_hmm_label.grid(row=4, column=0, columnspan=2, pady=5)

            # Now you can configure the label's text
            self.load_hmm_label.config(text=f"Loaded model: {os.path.basename(loaded_model_filename)}")

        self.create_model_selection_window()

    def create_model_selection_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("RL Model Selection")
        self.window.transient(self.parent)  # Keep window on top of parent

         # Initialize algorithm_names here, AFTER initialize_algorithms and get_available_algorithms
        self.algorithm_params = initialize_algorithms()  # Assign the returned dictionary
        self.algorithms = get_available_algorithms()  # No need to pass rl_algorithms here
        algorithm_names = list(self.algorithms.keys())

        ttk.Label(self.window, text="Select Algorithm:").grid(
            row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.algorithm_var = tk.StringVar(
            value=self.algorithm_settings['selected_algorithm'])

        # Initialize algorithm_names here, AFTER initialize_algorithms and get_available_algorithms
        algorithm_names = list(self.algorithms.keys())

        self.algorithm_combobox = ttk.Combobox(
            self.window,
            textvariable=self.algorithm_var,
            values=algorithm_names)
        self.algorithm_combobox.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        self.update_algorithm_dropdown()

        # Add a checkbox for enabling/disabling HMM
        self.use_hmm_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.window,
                        text="Use HMM",
                        variable=self.use_hmm_var).grid(row=1,
                                                        column=0,
                                                        columnspan=2,
                                                        pady=5)

        # Add a button for training the HMM
        self.train_hmm_button = ttk.Button(self.window,
                                          text="Train HMM",
                                          command=self.train_hmm,
                                          state=tk.DISABLED)
        self.train_hmm_button.grid(row=2, column=0, pady=5, sticky=tk.W)

        # Add a button for loading the HMM with an associated label
        self.load_hmm_button = ttk.Button(self.window,
                                          text="Load HMM",
                                          command=self.load_hmm,
                                          state=tk.DISABLED)
        self.load_hmm_button.grid(row=3, column=0, pady=5, sticky=tk.W)

        self.load_hmm_label = ttk.Label(self.window, text="")
        self.load_hmm_label.grid(row=3, column=1, pady=5, sticky=tk.E)

        # Add a label to display the loaded model filename
        self.load_hmm_label = ttk.Label(self.window, text="")  # Now create the label here
        self.load_hmm_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Trace the checkbox to enable/disable the buttons
        self.use_hmm_var.trace_add("write", self.toggle_train_hmm_button)

        settings_button = ttk.Button(self.window,
                                    text="Settings",
                                    command=self.open_algorithm_settings)
        settings_button.grid(row=5, column=0, columnspan=2, pady=10)

        save_button = ttk.Button(self.window,
                                text="Save",
                                command=self.save_model_selection)
        save_button.grid(row=6, column=0, pady=10, sticky=tk.W)

        default_button = ttk.Button(self.window,
                                    text="Default Settings",
                                    command=self.reset_to_default)
        default_button.grid(row=6, column=1, pady=10, sticky=tk.E)

    def open_algorithm_settings(self):
        from rl_gui.algorithm_settings_gui import AlgorithmSpecificSettingsWindow  
        algorithm = self.algorithm_var.get()
        if algorithm.lower() in self.algorithm_params:
            params = self.algorithm_params[algorithm.lower()]
            AlgorithmSpecificSettingsWindow(self.window, self, algorithm, self.algorithm_settings, params)
        else:
            messagebox.showerror("Error", f"No parameters found for algorithm: {algorithm}")

    def update_algorithm_dropdown(self):
        algorithm_names = list(self.algorithms.keys())
        self.algorithm_combobox['values'] = algorithm_names
        if algorithm_names:  # Check if algorithm_names is not empty
            self.algorithm_var.set(algorithm_names[0])  # Set the first algorithm as the default

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

####################### HMM Training Functionality #######################
    def toggle_train_hmm_button(self, *args):
        if self.use_hmm_var.get():
            self.train_hmm_button.config(state=tk.NORMAL)
            self.load_hmm_button.config(state=tk.NORMAL)  # Enable Load HMM button
        else:
            self.train_hmm_button.config(state=tk.DISABLED)
            self.load_hmm_button.config(state=tk.DISABLED)  # Disable Load HMM button

    def train_hmm(self):
        train_hmm_model()

    def load_hmm(self):
        # Set the initial directory for the file dialog
        user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
        initial_dir = os.path.join(user_data_path, 'HMMmodel')

        # Open a file dialog for the user to select the model file
        model_filename = filedialog.askopenfilename(
            initialdir=initial_dir,
            defaultextension=".pkl",
            filetypes=[("Pickle Files", "*.pkl"), ("All Files", "*.*")])
        if not model_filename:
            return  # User canceled the dialog

        try:
            import pickle
            with open(model_filename, 'rb') as file:
                model = pickle.load(file)
            # ... use the loaded model in your AI algorithm ...

            # Update the label with the loaded model filename
            self.loaded_model_label.config(
                text=f"Loaded model: {os.path.basename(model_filename)}")
            
            # Save the loaded model filename to settings
            self.algorithm_settings['loaded_hmm_model'] = model_filename
            self.save_to_file()  # Save the updated settings

            messagebox.showinfo("Success", "HMM loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load HMM model: {e}")

# Example usage
def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    algorithm_settings = {}
    app = RLModelSelectionWindow(root, algorithm_settings)
    root.mainloop()

if __name__ == "__main__":
    main()
