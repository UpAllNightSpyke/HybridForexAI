import os
import json
from ai_env import TradingEnv
from normalize_data import normalize_data
from rl_algorithms.functions import get_available_algorithms, initialize_algorithms
from appdirs import user_data_dir
import pandas as pd
import re  # Import the re module for regular expression matching

def main():
    # 1. Load Settings (only for algorithm selection)
    user_data_path = user_data_dir("RLNNApp", "UpAllNightSpyke")
    settings_file = os.path.join(user_data_path, 'settings', 'algorithm_settings.json')
    with open(settings_file, 'r') as f:
        settings = json.load(f)
    selected_algorithm = settings['selected_algorithm'].upper()  # Ensure uppercase for consistency

    # 2. Prepare Data
    normalized_data_dir = os.path.join(user_data_path, 'forex_data', 'normalized')

    # Find the normalized data file
    for filename in os.listdir(normalized_data_dir):
        if filename.endswith("_normalized.csv"):
            normalized_data_file = os.path.join(normalized_data_dir, filename)
            break
    else:
        raise FileNotFoundError("No normalized data file found.")

    # Extract symbol and timeframe from filename
    match = re.match(r"(.+)_(\w+)_normalized\.csv", filename)
    if match:
        symbol, timeframe = match.groups()
    else:
        raise ValueError(f"Could not extract symbol and timeframe from filename: {filename}")

    # Load the normalized data into a DataFrame
    normalized_data = pd.read_csv(normalized_data_file)

    # 3. Create Trading Environment
    env = TradingEnv(normalized_data, symbol, timeframe)  # Pass necessary data to your env

    # 4. Initialize RL Algorithm
    rl_algorithms = {}
    algorithm_params = {}
    initialize_algorithms(rl_algorithms, algorithm_params)
    algorithms = get_available_algorithms(rl_algorithms)
    algorithm_func = algorithms.get(selected_algorithm)
    if algorithm_func is None:
        raise ValueError(f"Invalid algorithm selected: {selected_algorithm}")

    # 5. Create RL Agent Instance 
    agent = algorithm_func(env, **settings.get(selected_algorithm, {}).get('params', {}))  # Pass algorithm parameters, handle missing keys

    # 6. Train RL Agent
    total_timesteps = 1000  # Replace with your desired number of training timesteps
    for timestep in range(1, total_timesteps + 1):
        agent.learn(total_timesteps=1)  # Train for one timestep
        if timestep % 100 == 0:  # Print progress every 100 timesteps
            print(f"Training progress: {timestep}/{total_timesteps} timesteps")

    # 7. (Optional) Evaluate and Save Agent
    # ... (add code to evaluate the trained agent, e.g., on a test dataset)
    # ... (save the trained agent if needed)

if __name__ == "__main__":
    main()
