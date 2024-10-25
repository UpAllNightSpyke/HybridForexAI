import os
import importlib
import json

#CACHE_FILE = os.path.join(os.path.dirname(__file__), 'algorithm_cache.json') Moved to initialize_algorithms()

rl_algorithms = {}  # Initialize as a dictionary
algorithm_params = {}

def get_available_algorithms():
    initialize_algorithms()
    return rl_algorithms

def initialize_algorithms():
    global rl_algorithms, algorithm_params

    CACHE_FILE = os.path.join(os.path.dirname(__file__), 'algorithm_cache.json')

    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as file:
                cache = json.load(file)
                # Load algorithm functions from cache
                for alg in cache['algorithms']:
                    try:
                        module_path = cache['algorithm_params'][alg.lower()]['module_path']  # Get module path
                        module = importlib.import_module(module_path)  # Import the module
                        func_name = f"train_{alg.lower()}"  # Construct function name
                        rl_algorithms[alg.upper()] = getattr(module, func_name)  # Get function from module
                        print(f"Loaded {alg} from cache.")
                    except Exception as e:
                        print(f"Error loading {alg} from cache: {e}")
                algorithm_params.update(cache['algorithm_params'])
                print("Loaded algorithms and parameters from cache.")
        except Exception as e:
            print(f"Error loading cache: {e}")

    current_dir = os.path.dirname(__file__)

    print("Starting algorithm initialization...")

    for category in ['value_based', 'policy_based', 'model_based']:
        print(f"Searching category: {category}") 
        for filename in os.listdir(os.path.join(current_dir, category)):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]
                print(f"Found module: {module_name}.py")

                try:
                    module = importlib.import_module(f'.{category}.{module_name}', package='rl_algorithms')
                    print(f"Imported module: {category}.{module_name}") 

                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if callable(attr) and attr_name.startswith('train_'):
                            algorithm_name = attr_name.replace('train_', '').upper()
                            rl_algorithms[algorithm_name] = attr  # Store the function
                            print(f"   Imported {algorithm_name} function from {category}/{module_name}.py")

                    if hasattr(module, 'algorithm_params'):
                        algorithm_params[module_name] = getattr(module, 'algorithm_params')
                        # Add module path to algorithm_params
                        algorithm_params[module_name]['module_path'] = f"rl_algorithms.{category}.{module_name}"
                        print(f"   Imported parameters for {category}/{module_name}.py") 

                except Exception as e:
                    print(f"Error importing module {category}.{module_name}: {e}") 

    with open(CACHE_FILE, 'w') as file:
        json.dump({'algorithms': list(rl_algorithms.keys()), 'algorithm_params': algorithm_params}, file)
    print("Cached algorithms and parameters.")
    print(f"Available algorithms: {rl_algorithms}")

    return algorithm_params
