import os
import importlib
import json

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'algorithm_cache.json')

global rl_algorithms, algorithm_params
rl_algorithms = {}
algorithm_params = {}

def initialize_algorithms():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            cache = json.load(file)
            global rl_algorithms, algorithm_params
            rl_algorithms = {alg.upper(): None for alg in cache['algorithms']}
            algorithm_params = cache['algorithm_params']
            print("Loaded algorithms and parameters from cache.")
            return

    current_dir = os.path.dirname(__file__)

    for filename in os.listdir(current_dir):
        if filename.endswith('.py') and filename != 'functions.py' and filename != '__init__.py':
            module_name = filename[:-3]  # Remove the .py extension
            module = importlib.import_module(f'.{module_name}', package='rl_algorithms')
            
            # Get all functions in the module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and attr_name.startswith('train_'):
                    # Add the function to the dictionary
                    algorithm_name = attr_name.replace('train_', '').upper()
                    rl_algorithms[algorithm_name] = attr
                    print(f"Imported {algorithm_name} function from {module_name}.py")
            
            # Get the algorithm_params from the module
            if hasattr(module, 'algorithm_params'):
                algorithm_params[module_name] = getattr(module, 'algorithm_params')
                print(f"Imported parameters for {module_name}.py")

    # Cache the results
    with open(CACHE_FILE, 'w') as file:
        json.dump({'algorithms': list(rl_algorithms.keys()), 'algorithm_params': algorithm_params}, file)
    print("Cached algorithms and parameters.")

def get_available_algorithms():
    return list(rl_algorithms.keys()), algorithm_params

# Initialize algorithms on import
initialize_algorithms()