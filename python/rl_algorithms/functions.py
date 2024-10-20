import os
import importlib
import json

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'algorithm_cache.json')

# Moved these lines into the initialize_algorithms function to avoid circular import issues
# global rl_algorithms, algorithm_params
# rl_algorithms = {}
# algorithm_params = {}
# 
# rl_algorithms = {}  # Initialize as a dictionary

def initialize_algorithms():
    global rl_algorithms, algorithm_params

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            cache = json.load(file)
            # No need to redeclare global here
            rl_algorithms = {alg.upper(): None for alg in cache['algorithms']}
            algorithm_params = cache['algorithm_params']
            print("Loaded algorithms and parameters from cache.")
            return

    current_dir = os.path.dirname(__file__)

    print("Starting algorithm initialization...")  # Debug print

    # Loop through algorithm categories
    for category in ['value_based', 'policy_based', 'model_based']:
        print(f"Searching category: {category}")  # Debug print
        for filename in os.listdir(os.path.join(current_dir, category)):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]
                print(f"Found module: {module_name}.py")

                if module_name == 'a2c':
                    print(f"Importing A2C module: {category}.{module_name}")

                try:
                    module = importlib.import_module(f'.{category}.{module_name}', package='rl_algorithms')
                    print(f"Imported module: {category}.{module_name}")  # Debug print

                    # Get all functions in the module
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if callable(attr) and attr_name.startswith('train_'):
                            # Add the function to the dictionary
                            algorithm_name = attr_name.replace('train_', '').upper()
                            rl_algorithms[algorithm_name] = attr
                            print(f"   Imported {algorithm_name} function from {category}/{module_name}.py")  # Debug print

                    # Get the algorithm_params from the module
                    if hasattr(module, 'algorithm_params'):
                        algorithm_params[module_name] = getattr(module, 'algorithm_params')
                        print(f"   Imported parameters for {category}/{module_name}.py")  # Debug print

                except Exception as e:
                    print(f"Error importing module {category}.{module_name}: {e}")  # Debug print

    # Cache the results
    with open(CACHE_FILE, 'w') as file:
        json.dump({'algorithms': list(rl_algorithms.keys()), 'algorithm_params': algorithm_params}, file)
    print("Cached algorithms and parameters.")
    print(f"Available algorithms: {rl_algorithms}")  # Debug print

def get_available_algorithms(rl_algorithms):
    return rl_algorithms

# Initialize algorithms on import removed for circular import issues
#initialize_algorithms()