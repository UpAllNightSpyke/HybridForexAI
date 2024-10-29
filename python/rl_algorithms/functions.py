import os
import importlib
from appdirs import user_data_dir
from lxml import etree

rl_algorithms = {}  # Initialize as a dictionary
algorithm_params = {}

def get_available_algorithms(rl_algorithms={}):
    initialize_algorithms()
    print("rl_algorithms in get_available_algorithms:", rl_algorithms)
    return rl_algorithms

def initialize_algorithms():
    print("Initializing algorithms...")
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

            print("Root tag:", root.tag)  # Print the root tag of the XML file
            algorithm_elements = root.findall("algorithm")
            print("Number of algorithm elements found:", len(algorithm_elements))  # Print the number of algorithm elements

            for alg_element in root.findall("algorithm"):
                alg_name = alg_element.get("name")
                category = alg_element.get("category")
                module_path = alg_element.find("module_path").text

                print(f"Algorithm name: {alg_name}") # Print alg_name
                print(f"Module path: {module_path}") # Print module_path

                try:
                    # Import the module and class dynamically
                    print(f"Attempting to import module: {module_path}")
                    module = importlib.import_module(module_path)
                    print(f"Imported module: {module_path}")

                    class_name = alg_name.replace("TRAIN_", "")
                    print(f"Class name: {class_name}") # Print class_name
                    print(f"Attempting to get class: {class_name} from {module_path}")
                    rl_algorithms[alg_name] = getattr(module, class_name)  # Store the class
                    print(f"Successfully got class: {class_name} from {module_path}")

                except Exception as e: # Catch all exceptions
                    print(f"Error loading algorithm {alg_name} from {module_path}: {e}")
                except ModuleNotFoundError as e:
                    print(f"Error importing module {module_path}: {e}")
                except AttributeError as e:
                    print(f"Error getting class {class_name} from {module_path}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred while loading {alg_name}: {e}")

            algorithm_params = {}
            for param_element in root.find("parameters").findall("param"):
                alg_name = param_element.get("name")
                algorithm_params[alg_name] = {}
                for p in param_element.findall("parameter"):
                    algorithm_params[alg_name][p.get("name")] = p.text

            print("Loaded algorithms and parameters from cache.")
            return algorithm_params

        except Exception as e:
            print(f"Error loading cache: {e}")

    current_dir = os.path.dirname(__file__)
    print(f"Current directory: {current_dir}")  # Print current directory

    print("Starting algorithm initialization...")

    for category in ['value_based', 'policy_based', 'model_based']:
        print(f"Searching category: {category}")
        category_path = os.path.join(current_dir, category)
        print(f"Category path: {category_path}")  # Print category path
        for filename in os.listdir(category_path):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]
                print(f"Found module: {module_name}.py")

                try:
                    print(f"Attempting to import module: rl_algorithms.{category}.{module_name}")  # Print import statement
                    module = importlib.import_module(f"rl_algorithms.{category}.{module_name}")
                    print(f"Imported module: rl_algorithms.{category}.{module_name}")

                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and attr_name.startswith('Train_'):  # Check if it's a class
                            algorithm_name = attr_name.replace('Train_', '').upper()
                            rl_algorithms[algorithm_name] = attr  # Store the class
                            print(f"  Imported {algorithm_name} class from {category}/{module_name}.py")

                            if hasattr(module, 'algorithm_params'):
                                algorithm_params[module_name] = getattr(module, 'algorithm_params')
                                # Add module path to algorithm_params
                                algorithm_params[module_name]['module_path'] = f"rl_algorithms.{category}.{module_name}"
                                print(f"  Imported parameters for {category}/{module_name}.py")

                except Exception as e:
                        print(f"Error importing module rl_algorithms.{category}.{module_name}: {e}")
        else:
            print(f"Category directory not found: {category_path}")
    
    print("rl_algorithms before saving:", rl_algorithms)  # Print rl_algorithms

    # Create the XML structure
    root = etree.Element("cache")
    algorithms_element = etree.SubElement(root, "algorithms")
    for alg_name, cls in rl_algorithms.items():  # Iterate over classes
        alg_element = etree.SubElement(
            algorithms_element,
            "algorithm",
            name=alg_name,
            category=cls.__module__.split('.')[-2])  # Add category attribute
        etree.SubElement(alg_element,
                         "module_path").text = cls.__module__  # Store the full module path

    params_element = etree.SubElement(root, "parameters")
    for alg_name, params in algorithm_params.items():
        param_element = etree.SubElement(params_element, "param", name=alg_name)
        for param_name, param_value in params.items():
            etree.SubElement(param_element, "parameter",
                             name=param_name).text = str(param_value)

    print(
        "XML structure before saving:", etree.tostring(root, pretty_print=True)
    )  # Print XML structure before saving

    try:
        # Save the XML cache
        tree = etree.ElementTree(root)
        tree.write(CACHE_FILE, pretty_print=True)
    except Exception as e:
        print(f"Error saving cache file: {e}")

    print("Cached algorithms and parameters.")
    return algorithm_params