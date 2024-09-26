import importlib
import os

# Initialize the dictionary to hold indicator functions
indicator_functions = {}

# Get the directory of the current file
current_dir = os.path.dirname(__file__)

# Iterate over all files in the indicators directory
for filename in os.listdir(current_dir):
    if filename.endswith('.py') and filename != 'functions.py' and filename != '__init__.py':
        module_name = filename[:-3]  # Remove the .py extension
        module = importlib.import_module(f'.{module_name}', package='indicators')
        
        # Get all functions in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and attr_name.startswith('calculate_'):
                # Add the function to the dictionary
                indicator_name = attr_name.replace('calculate_', '').capitalize()
                indicator_functions[indicator_name] = attr

def get_available_indicators():
    return list(indicator_functions.keys())