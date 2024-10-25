import os
import json
from appdirs import user_data_dir
import pandas as pd
from rl_algorithms.functions import initialize_algorithms, get_available_algorithms

def find_cleaned_data():
    """
    Locates the cleaned data file in the user data directory.

    Returns:
        str: The path to the cleaned data file.

    Raises:
        FileNotFoundError: If no cleaned data file is found.
    """
    user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
    cleaned_data_dir = os.path.join(user_data_path, 'forex_data', 'cleaned')

    for filename in os.listdir(cleaned_data_dir):
        if filename.endswith("_cleaned.csv"):
            cleaned_data_file = os.path.join(cleaned_data_dir, filename)
            return cleaned_data_file

    raise FileNotFoundError("No cleaned data file found.")

def train_rl_model(algorithm_type):
    """
    Trains the specified RL model using the cleaned data and saves it.
    """
    try:
        # 1. Load the cleaned data
        cleaned_data_file = find_cleaned_data()
        data = pd.read_csv(cleaned_data_file)

        # 2. Select relevant columns for RL training
        rl_data = data[['open', 'high', 'low', 'close', 'tick_volume']].values  # Select relevant columns

        # 3. Initialize the RL environment (you'll need to define this based on your project)
        env = YourRLEnvironment(rl_data)  # Replace YourRLEnvironment with your actual environment class

        # 4. Initialize and train the RL model
        algorithms = initialize_algorithms()
        algorithm = get_available_algorithms()[algorithm_type]
        model = algorithm(env)  # Instantiate the RL model
        model.learn(total_timesteps=10000)  # Adjust total_timesteps as needed

        # 5. Save the trained RL model
        user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
        model_dir = os.path.join(user_data_path, 'RLmodel')
        os.makedirs(model_dir, exist_ok=True)
        model_filename = os.path.join(model_dir, f'rl_model_{algorithm_type}.pkl')
        with open(model_filename, 'wb') as file:
            pickle.dump(model, file)

        print(f"RL model ({algorithm_type}) trained and saved successfully!")
    except Exception as e:
        print(f"An error occurred while training the RL model: {e}")

def load_rl_model(algorithm_type):
    """
    Loads the trained RL model of the specified type from the RLmodel directory.

    Returns:
        The trained RL model.

    Raises:
        FileNotFoundError: If the RL model file is not found.
    """
    try:
        user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
        model_dir = os.path.join(user_data_path, 'RLmodel')
        model_filename = os.path.join(model_dir, f'rl_model_{algorithm_type}.pkl')
        with open(model_filename, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        print(f"Trained RL model ({algorithm_type}) not found.")
        return None