import os
import importlib.util
from indicators.functions import get_available_indicators as get_indicators_with_params

def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_available_indicators(indicators_path):
    indicators = {}
    for file_name in os.listdir(indicators_path):
        if file_name.endswith('.py') and file_name != '__init__.py':
            module_name = file_name[:-3]  # Remove the .py extension
            module = import_module_from_file(module_name, os.path.join(indicators_path, file_name))
            indicators[module_name] = module
    print(f"Available indicators: {list(indicators.keys())}")  # Debug line
    
    # Get indicator names and their parameters
    indicator_names, indicator_params = get_indicators_with_params()
    return indicator_names, indicator_params