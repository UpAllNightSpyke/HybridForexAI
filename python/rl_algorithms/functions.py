import os
import importlib
from appdirs import user_data_dir
from lxml import etree

rl_algorithms = {}  # Initialize as a dictionary
algorithm_params = {}

def get_available_algorithms(rl_algorithms={}):
    initialize_algorithms()
    return rl_algorithms

def initialize_algorithms():
    global rl_algorithms, algorithm_params

    # Get the user data directory
    user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")

    # Define the cache file path within the user data directory
    CACHE_FILE = os.path.join(user_data_path, 'algorithm_cache.xml')

    if os.path.exists(CACHE_FILE):
        try:
            # Load algorithms and parameters from XML cache
            tree = etree.parse(CACHE_FILE)
            root = tree.getroot()

            rl_algorithms = {}
            for alg_element in root.findall("algorithm"):
                alg_name = alg_element.get("name")
                module_path = alg_element.find("module_path").text
                module = importlib.import_module(module_path)
                func_name = f"train_{alg_name.lower()}"
                rl_algorithms[alg_name] = getattr(module, func_name)

            algorithm_params = {}
            for param_element in root.find("parameters").findall("param"):
                alg_name = param_element.get("name")
                algorithm_params[alg_name] = {}
                for p in param_element.findall("parameter"):
                    algorithm_params[alg_name][p.get("name")] = p.text

            print("Loaded algorithms and parameters from cache.")
            print("Available algorithms:", rl_algorithms.keys())  # Print available algorithms
            return algorithm_params

        except Exception as e:
            print(f"Error loading cache: {e}")

    current_dir = os.path.dirname(__file__)

    print("Starting algorithm initialization...")

    for category in ['value_based', 'policy_based', 'model_based']:
        category_path = os.path.join(current_dir, category)
        if not os.path.exists(category_path):
            print(f"Category path does not exist: {category_path}")
            continue

        print(f"Searching category: {category}")
        for filename in os.listdir(category_path):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]
                print(f"Found module: {module_name}.py")

                try:
                    module = importlib.import_module(
                        f'rl_algorithms.{category}.{module_name}')
                    print(f"Imported module: {category}.{module_name}")

                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if callable(attr) and attr_name.startswith('train_'):
                            algorithm_name = attr_name.replace(
                                'train_', '').upper()
                            
                            # Store both the function and the class
                            rl_algorithms[algorithm_name] = attr  # Store the function
                            rl_algorithms[algorithm_name.replace("TRAIN_", "")] = getattr(module, algorithm_name.replace("TRAIN_", ""))  # Store the class
                            
                            print(
                                f"   Imported {algorithm_name} function from {category}/{module_name}.py"
                            )

                        if hasattr(module, 'algorithm_params'):
                            algorithm_params[
                                module_name] = getattr(module,
                                                       'algorithm_params')
                            # Add module path to algorithm_params
                            algorithm_params[module_name][
                                'module_path'] = f"rl_algorithms.{category}.{module_name}"
                            print(
                                f"   Imported parameters for {category}/{module_name}.py"
                            )

                except Exception as e:
                    print(
                        f"Error importing module {category}.{module_name}: {e}"
                    )

    # Create the XML structure
    root = etree.Element("cache")
    algorithms_element = etree.SubElement(root, "algorithms")
    for alg_name, func in rl_algorithms.items():
        alg_element = etree.SubElement(algorithms_element, "algorithm", name=alg_name)
        etree.SubElement(alg_element, "module_path").text = func.__module__

    params_element = etree.SubElement(root, "parameters")
    for alg_name, params in algorithm_params.items():
        param_element = etree.SubElement(params_element, "param", name=alg_name)
        for param_name, param_value in params.items():
            etree.SubElement(param_element, "parameter", name=param_name).text = str(param_value)

    # Save the XML cache
    tree = etree.ElementTree(root)
    tree.write(CACHE_FILE, pretty_print=True)

    print("Cached algorithms and parameters.")
    print("Available algorithms:", rl_algorithms.keys())  # Print available algorithms
    return algorithm_params