import tkinter as tk
from tkinter import messagebox
import json
from cryptography.fernet import Fernet
import os

# Define the key file path
key_file_path = 'encryption_key.key'

# Check if the key file exists
if not os.path.exists(key_file_path):
    # Generate a new key and save it to the file
    key = Fernet.generate_key()
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)
else:
    # Load the key from the file
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()

cipher_suite = Fernet(key)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

def open_account_window():
    account_window = tk.Toplevel()
    account_window.title("Account Input GUI")

    tk.Label(account_window, text="Account:").grid(row=0, column=0, padx=5, pady=5)
    account_entry = tk.Entry(account_window)
    account_entry.grid(row=0, column=1, padx=5, pady=5)
    account_entry.insert(0, "3021640")  # Default value for Account

    tk.Label(account_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(account_window, show='*')
    password_entry.grid(row=1, column=1, padx=5, pady=5)
    password_entry.insert(0, "AItester1!")  # Default value for Password

    tk.Label(account_window, text="Server:").grid(row=2, column=0, padx=5, pady=5)
    server_entry = tk.Entry(account_window)
    server_entry.grid(row=2, column=1, padx=5, pady=5)
    server_entry.insert(0, "PlexyTrade-Server01")  # Default value for Server

    tk.Label(account_window, text="MT5 Path:").grid(row=3, column=0, padx=5, pady=5)
    mt5_path_entry = tk.Entry(account_window)
    mt5_path_entry.grid(row=3, column=1, padx=5, pady=5)
    mt5_path_entry.insert(0, "C:\\Program Files\\PlexyTrade MT5 Terminal\\terminal64.exe")  # Default value for MT5 Path

    def on_submit():
        account_settings = {
            'account': encrypt_data(account_entry.get()),
            'password': encrypt_data(password_entry.get()),
            'server': encrypt_data(server_entry.get()),
            'mt5_path': encrypt_data(mt5_path_entry.get())
        }
        
        with open('account_settings.json', 'w') as f:
            json.dump(account_settings, f)
        
        messagebox.showinfo("Success", "Account settings saved successfully!")
        account_window.destroy()

    tk.Button(account_window, text="Submit", command=on_submit).grid(row=4, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    open_account_window()
    root.mainloop()