import importlib
import os

# Initialize the dictionary to hold indicator functions and their parameters
indicator_functions = {}
indicator_params = {}

def initialize_indicators():
    global indicator_functions, indicator_params
    current_dir = os.path.dirname(__file__)

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
                    print(f"Imported {indicator_name} function from {module_name}.py")
            
            # Get the indicator_params from the module
            if hasattr(module, 'indicator_params'):
                indicator_params[module_name] = getattr(module, 'indicator_params')
                print(f"Imported parameters for {module_name}.py")

def get_available_indicators():
    return list(indicator_functions.keys()), indicator_params