import tkinter as tk
from tkinter import ttk
import json
from cryptography.fernet import Fernet
import os
from appdirs import user_data_dir  # Import for user data directory
from tkinter import ttk, filedialog  # Import filedialog

class AccountWindow:
    def __init__(self, parent, account_details, user_data_dir):  # Pass user_data_dir
        self.parent = parent
        self.account_details = account_details
        self.user_data_dir = user_data_dir  # Store user_data_dir
        self.create_account_window()

    def create_account_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Account Details")

        self.account_fields = {
            'MT5 Path': tk.StringVar(value=self.account_details.get('MT5 Path', '')),
            'Account': tk.StringVar(value=self.account_details.get('Account', '')),
            'Password': tk.StringVar(value=self.account_details.get('Password', '')),
            'Server': tk.StringVar(value=self.account_details.get('Server', ''))
        }

        for idx, (label, var) in enumerate(self.account_fields.items()):
            ttk.Label(self.window, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)

            if label == 'MT5 Path':
                # Create Entry widget for MT5 Path
                entry = ttk.Entry(self.window, textvariable=var)
                entry.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.EW)

                # Create Browse button for MT5 Path
                browse_button = ttk.Button(self.window, text="Browse", command=self.browse_mt5_path)
                browse_button.grid(row=idx, column=2, padx=5, pady=5)
            else:
                # Create Entry widgets for other fields
                ttk.Entry(self.window, textvariable=var, show="*" if label == 'Password' else "").grid(row=idx, column=1, padx=10, pady=5, sticky=tk.EW)

        save_button = ttk.Button(self.window, text="Save", command=self.save_account_details)
        save_button.grid(row=len(self.account_fields), column=0, columnspan=3, pady=10)  # Span 3 columns

    def browse_mt5_path(self):
        """Opens a file dialog to select the MT5 terminal executable."""
        file_path = filedialog.askopenfilename(
            initialdir="C:\\Program Files\\",  # You can set a more appropriate initial directory
            title="Select MT5 Terminal Executable",
            filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*"))
        )
        if file_path:
            self.account_fields['MT5 Path'].set(file_path)

    def save_account_details(self):
        for label, var in self.account_fields.items():
            self.account_details[label] = var.get()

        # Encrypt and save account details
        self.encrypt_and_save_account_details()
        self.window.destroy()

    def encrypt_and_save_account_details(self):
        # Load or generate encryption key
        key = self.load_or_generate_key()
        cipher_suite = Fernet(key)

        # Convert account details to JSON string
        account_details_json = json.dumps(self.account_details).encode('utf-8')

        # Encrypt the JSON string
        encrypted_data = cipher_suite.encrypt(account_details_json)

        # Save the encrypted data to the 'settings' directory
        account_file = os.path.join(self.user_data_dir, 'settings', 'account_settings.json')  # Update path
        with open(account_file, 'wb') as f:
            f.write(encrypted_data)

        print("Account details saved and encrypted successfully.")

    def load_or_generate_key(self):
        # Use user data directory for the key file
        key_file = os.path.join(self.user_data_dir, 'settings', 'account_key.key')

        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
            print("Encryption key loaded successfully.")
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            print("New encryption key generated and saved successfully.")

        return key